import abc
import itertools
import logging
import os
import sys
from collections import defaultdict
from enum import Enum

from typing import Union, List, Any, Callable, Type, Dict, Set, TypeVar

from yattag import Doc

from pytconf.color_utils import print_highlight, color_hi, print_title, color_ok, color_warn, print_error
from pytconf.convert import convert_str_to_int, convert_int_to_str, convert_str_to_int_default, \
    convert_str_to_list_int, convert_list_int_to_str, convert_list_str_to_str, \
    convert_str_to_list_str, convert_str_to_int_or_none, \
    convert_int_or_none_to_str, convert_str_to_bool, convert_bool_to_str, convert_str_to_str, \
    convert_str_to_str_or_none, convert_str_or_none_to_str
from pytconf.enum_subset import EnumSubset
from pytconf.errors_collector import ErrorsCollector
from pytconf.extended_enum import str_to_enum_value, enum_type_to_list_str

PARAMS_ATTRIBUTE = "_params"
DEFAULT_GROUP_NAME: str = "default"
SPECIAL_COMMANDS = {"help", "help-suggest", "help-all"}


class MetaConfig(type):
    """
    base class for all configs
    """

    def __new__(mcs, name, bases, cls_dict):
        if name != "Config":
            params_dict = dict()
            cls_dict[PARAMS_ATTRIBUTE] = params_dict
            for k, d in cls_dict.items():
                if isinstance(d, Param):
                    # assert d.default is not NO_DEFAULT
                    params_dict[k] = d
                    cls_dict[k] = d.default
        return type.__new__(mcs, name, bases, cls_dict)

    def __init__(cls, name, bases, cls_dict):
        # print(name, bases, cls_dict)
        # if len(cls.mro()) > 2:
        #     register_config(cls, name)
        #     # print("was subclassed by " + name)
        if name != "Config":
            # noinspection PyTypeChecker
            get_pytconf().register_config(cls, name)
        # print(name, cls_dict)
        super(MetaConfig, cls).__init__(name, bases, cls_dict)


ParamType = TypeVar('ParamType', bound='Param')


class Config(metaclass=MetaConfig):
    """
        base class for all configs
    """

    @classmethod
    def get_attributes(cls: Any) -> List[str]:
        return getattr(cls, PARAMS_ATTRIBUTE).keys()
        # return [attr for attr in dir(cls) if not callable(getattr(cls, attr))
        #        and not attr.startswith("__")]

    @classmethod
    def get_params(cls: Any) -> Dict[str, ParamType]:
        return getattr(cls, PARAMS_ATTRIBUTE)

    @classmethod
    def get_param_by_name(cls: Any, name: str) -> ParamType:
        return cls.get_params()[name]


class HtmlGen(object):
    def __init__(self):
        document, tag, text, line = Doc().ttl()
        self.document = document
        self.tag = tag
        self.text = text
        self.line = line


class PytconfConf(object):
    def __init__(self):
        self._configs = set()
        self._config_names = set()
        self.main_function = None
        self.function_name_to_configs: Dict[str, List[Type[Config]]] = dict()
        self.function_name_to_suggest_configs: Dict[str, List[Type[Config]]] = dict()
        self.function_name_to_callable: Dict[str, Callable] = dict()
        self.function_group_names: Dict[str, Set[str]] = defaultdict(set)
        self.allow_free_args: Dict[str, bool] = dict()
        self.function_group_descriptions: Dict[str, str] = dict()
        self.function_group_list = []
        self.attribute_to_config: Dict[str, Type[Config]] = dict()
        self.free_args: List[str] = []
        self.app_name: Union[str, None] = None

    def register_main(self, f):
        self.main_function = f

    def register_config(self, config: Type[Config], name):
        """
        register a configuration class
        :param config:
        :param name:
        :return:
        """
        self._configs.add(config)
        self._config_names.add(name)
        # update the attributes_to_config map
        for attribute in config.get_attributes():
            if attribute in self.attribute_to_config:
                raise ValueError("pytconf: attribute [{}] appears more than once".format(attribute))
            self.attribute_to_config[attribute] = config

    @classmethod
    def print_errors(cls, errors: ErrorsCollector) -> None:
        for error in errors.errors:
            print_error(error)

    def show_help(self) -> None:
        print("Usage: {} [OPTIONS] COMMAND [ARGS]...".format(self.app_name))
        doc = self.main_function.__doc__
        if doc is not None:
            print()
            doc = doc.strip()
            doc = "\n".join(map(lambda x: "  {}".format(x.strip()), doc.split("\n")))
            print_highlight("{}".format(doc))
        print()
        print("Options:")
        print("  --help         Show mandatory help")
        print("  --help-suggest Show mandatory+suggestions help")
        print("  --help-all    Show all help")
        print()
        print("Commands:")
        for function_group in self.function_group_list:
            description = self.function_group_descriptions[function_group]
            print("  {}: {}".format(function_group, description))
            for name in sorted(self.function_group_names[function_group]):
                f = self.function_name_to_callable[name]
                doc = f.__doc__
                if doc is None:
                    print_highlight("    {}".format(name))
                else:
                    doc = doc.strip()
                    print("    {}: {}".format(color_hi(name), doc))
            print()

    def show_help_for_function(self, function_name: str, show_help_full: bool, show_help_suggest: bool) -> None:
        print("Usage: {} {} [OPTIONS] [ARGS]...".format(
            self.app_name,
            function_name,
        ))
        function_selected = self.function_name_to_callable[function_name]
        doc = function_selected.__doc__
        if doc is not None:
            doc = doc.strip()
            print()
            print_highlight("  {}".format(doc))
        print()
        print("Options:")
        print()
        for config in self.function_name_to_configs[function_name]:
            self.show_help_for_config(config)
        if show_help_suggest:
            for config in self.function_name_to_suggest_configs[function_name]:
                self.show_help_for_config(config)
        if show_help_full:
            for config in self._configs:
                self.show_help_for_config(config)

    @classmethod
    def show_help_for_config(cls, config):
        if config == Config:
            return
        doc = config.__doc__
        if doc is not None:
            doc = doc.strip()
            print_title("  {}".format(doc))
        else:
            print_title("  Undocumented parameter set")
        for name, param in config.get_params().items():
            if param.default is NO_DEFAULT:
                default = color_warn("MANDATORY")
            else:
                default = color_ok(param.t2s(param.default))
            print("    {} [{}]: {} [{}]".format(
                color_hi(name),
                param.get_type_name(),
                param.help_string,
                default,
            ))
            more_help = param.more_help()
            if more_help is not None:
                print("      {}".format(more_help))
        print()

    def process_flags(
        self,
        command_selected: str,
        flags: Dict[str, str],
        errors: ErrorsCollector,
    ) -> None:
        """
        Parse the args and fill the global data
        :param command_selected:
        :param flags:
        :param errors:
        """

        # set the flags into the "default" field and collect unknown flags
        unknown_flags = []
        for flag_raw, value in flags.items():
            if flag_raw not in self.attribute_to_config:
                unknown_flags.append(flag_raw)
                continue
            config = self.attribute_to_config[flag_raw]
            param = config.get_param_by_name(flag_raw)
            edit = value.startswith('=')
            if edit:
                v = param.s2t_generate_from_default(value[1:])
            else:
                v = param.s2t(value)
            setattr(config, flag_raw, v)
        if unknown_flags:
            errors.add_error("unknown flags [{}]".format(",".join(unknown_flags)))

        # check for missing parameters
        missing_parameters = []
        configs = self.function_name_to_configs[command_selected]
        for config in configs:
            for attribute in config.get_attributes():
                value = getattr(config, attribute)
                if value is NO_DEFAULT:
                    missing_parameters.append(attribute)
        if missing_parameters:
            errors.add_error("missing parameters [{}]".format(",".join(missing_parameters)))

        # move all default values to place (this will not be needed in the new scheme)
        for config in itertools.chain(configs, self._configs):
            for attribute in config.get_attributes():
                param: Param = getattr(config, attribute)
                if isinstance(param, Param):
                    if param.default is not NO_DEFAULT:
                        setattr(config, attribute, param.default)

    def config_arg_parse_and_launch(
        self,
        args: Union[List[str], None] = None,
        launch=True
    ) -> None:
        # if we are given no args then take the from sys.argv
        if args is None:
            args = sys.argv

        # we don't need the first argument which is the script path
        if args:
            self.app_name = os.path.basename(args[0])
            args = args[1:]
        else:
            self.app_name = "UNKNOWN APP NAME"

        # name of arg and it's value
        flags: Dict[str, str] = dict()
        special_flags = set()
        errors = ErrorsCollector()
        self.free_args = []

        self.parse_args(args, errors, flags, special_flags)

        # handle help flags
        show_help = False
        show_help_full = False
        show_help_suggest = False

        if "help" in special_flags:
            show_help = True
        if "help-suggest" in special_flags:
            show_help = True
            show_help_suggest = True
        if "help-all" in special_flags:
            show_help = True
            show_help_full = True

        # find the selected command
        command_selected = None

        # if there are free args then the command is the first of these
        if len(self.free_args) >= 1:
            command = self.free_args.pop(0)
            if command in self.function_name_to_callable:
                command_selected = command
            else:
                errors.add_error("unknown command [{}]".format(command))

        # if there are no free args and just one function then this is it
        if len(self.function_name_to_callable) == 1:
            command_selected = list(self.function_name_to_callable.keys())[0]

        # check if we are not allowed free args
        if command_selected is not None:
            if not self.allow_free_args[command_selected] and len(self.free_args) > 0:
                errors.add_error("free args are not allowed")

        if command_selected is None:
            if not show_help:
                errors.add_error("no command is selected")
        else:
            self.process_flags(command_selected, flags, errors)

        if errors.have_errors() and not show_help:
            self.print_errors(errors)
            return

        if show_help:
            if command_selected:
                self.show_help_for_function(command_selected, show_help_full, show_help_suggest)
            else:
                self.show_help()
            return

        if launch:
            function_to_run = self.function_name_to_callable[command_selected]
            function_to_run()

    def parse_args(self, args, errors, flags, special_flags):
        while args:
            current = args.pop(0)
            if current.startswith("--"):
                real = current[2:]
                number_of_equals = real.count("=")
                if number_of_equals == 1:
                    flag_name, flag_value = real.split("=")
                    flags[flag_name] = flag_value
                elif number_of_equals == 0:
                    if args:
                        more = args.pop(0)
                        flags[real] = more
                    elif real in SPECIAL_COMMANDS:
                        special_flags.add(real)
                    else:
                        errors.add_error("argument [{}] needs a follow-up argument".format(real))
                else:
                    errors.add_error("can not parse argument [{}]".format(real))
            else:
                self.free_args.append(current)

    def get_html(self) -> str:
        html_gen = HtmlGen()
        doc = self.main_function.__doc__
        assert doc is not None
        doc = doc.strip()
        html_gen.line('h1', doc)
        html_gen.line('h2', "API specifications")
        with html_gen.tag('ul'):
            for function_group_name in self.function_group_list:
                function_group_description = self.function_group_descriptions[function_group_name]
                html_gen.line('li', function_group_name, title='function group name: ')
                html_gen.line('li', function_group_description, title='function group description: ')
                with html_gen.tag('li'):
                    for function_name in sorted(self.function_group_names[function_group_name]):
                        self.get_html_for_function(function_name, html_gen)
        return html_gen.document.getvalue()

    def get_html_for_function(self, function_name, html_gen):
        with html_gen.tag('ul'):
            f = self.function_name_to_callable[function_name]
            if f.__doc__ is None:
                function_doc = "not description for this function"
            else:
                function_doc = f.__doc__.strip()
            html_gen.line('li', function_name, title='function name: ')
            html_gen.line('li', function_doc, title='function description: ')
            with html_gen.tag('li'):
                with html_gen.tag('ul'):
                    for config in self.function_name_to_configs[function_name]:
                        with html_gen.tag('li'):
                            self.get_html_for_config(config, html_gen)

    @classmethod
    def get_html_for_config(cls, config, html_gen):
        if config == Config:
            return
        if config.__doc__ is not None:
            doc = config.__doc__.strip()
        else:
            doc = "undocumented config"
        html_gen.line('h3', doc, title='config: ')
        with html_gen.tag('table'):
            for name, param in config.get_params().items():
                with html_gen.tag('tr'):
                    if param.default is NO_DEFAULT:
                        default = "MANDATORY"
                    else:
                        default = param.t2s(param.default)
                    if param.more_help() is None:
                        more_help = "No more help is documented"
                    else:
                        more_help = param.more_help()
                    html_gen.line('td', name)
                    html_gen.line('td', param.help_string)
                    html_gen.line('td', param.get_type_name())
                    html_gen.line('td', default)
                    html_gen.line('td', more_help)


_pytconf = PytconfConf()


def get_pytconf():
    return _pytconf


def config_arg_parse_and_launch(launch=True, args=None) -> None:
    """
    This is the real API
    """
    get_pytconf().config_arg_parse_and_launch(
        launch=launch,
        args=args,
    )


class Unique:
    pass


NO_DEFAULT = Unique()
NO_DEFAULT_TYPE = type(NO_DEFAULT)
NO_HELP = "No help for this configuration option"


class Param(object):
    __metaclass__ = abc.ABCMeta
    """
        Parent class of all parameters of configuration
    """

    def __init__(
        self,
        help_string=NO_HELP,
        default=NO_DEFAULT,
        type_name=None,
    ):
        super(Param, self).__init__()
        self.help_string = help_string
        self.default = default
        self.type_name = type_name

    def get_type_name(self):
        return self.type_name

    @abc.abstractmethod
    def s2t(self, s: str) -> object:
        pass

    def s2t_generate_from_default(self, s: str) -> object:
        raise ValueError("we do not support generation from default")

    @abc.abstractmethod
    def t2s(self, t: object) -> str:
        pass

    # noinspection PyMethodMayBeStatic
    def more_help(self) -> Union[str, None]:
        return None


class ParamFunctions(Param):
    """
    Parent class of all parameters of configuration
    """

    def __init__(
        self,
        help_string=NO_HELP,
        default=NO_DEFAULT,
        type_name=None,
        function_s2t: Callable = None,
        function_s2t_generate_from_default: Callable = None,
        function_t2s: Callable = None,
    ):
        super(ParamFunctions, self).__init__(
            help_string=help_string,
            default=default,
            type_name=type_name,
        )
        self.function_s2t = function_s2t
        self.function_t2s = function_t2s
        self.function_s2t_generate_from_default = function_s2t_generate_from_default

    def s2t(self, s: str) -> Any:
        return self.function_s2t(s)

    def s2t_generate_from_default(self, s: str) -> Any:
        return self.function_s2t_generate_from_default(self.default, s)

    def t2s(self, t: Any) -> str:
        return self.function_t2s(t)


class ParamFilename(Param):
    def __init__(
        self,
        help_string=NO_HELP,
        default=NO_DEFAULT,
        type_name=None,
        suffixes: List[str] = None,
    ):
        super(ParamFilename, self).__init__(
            help_string=help_string,
            default=default,
            type_name=type_name,
        )
        self.suffixes = suffixes

    def s2t(self, s):
        if self.suffixes is not None:
            assert any(s.endswith(x) for x in self.suffixes), "filename suffix is not accepted"
        return s

    def t2s(self, t):
        return t

    def more_help(self):
        if self.suffixes is None:
            return "no limitation on suffixes"
        else:
            return "allowed suffixes are {}".format(self.suffixes)


class ParamEnum(Param):
    def __init__(
        self,
        help_string=NO_HELP,
        default=NO_DEFAULT,
        enum_type: Type[Enum] = None,
    ):
        super(ParamEnum, self).__init__(
            help_string=help_string,
            default=default,
            type_name="enum",
        )
        self.enum_type = enum_type

    def get_type_name(self):
        return "Enum[{}]".format(self.enum_type.__name__)

    def s2t(self, s: str) -> Any:
        return str_to_enum_value(s, self.enum_type)

    def t2s(self, t: Any) -> str:
        return t.name

    def more_help(self):
        return "allowed values {}".format(enum_type_to_list_str(self.enum_type))


class ParamEnumSubset(Param):
    def __init__(
        self,
        help_string=NO_HELP,
        default=NO_DEFAULT,
        enum_type: Type[Enum] = None,
    ):
        super(ParamEnumSubset, self).__init__(
            help_string=help_string,
            default=default,
            type_name="enum",
        )
        self.enum_type = enum_type

    def get_type_name(self):
        return "EnumSubset[{}]".format(self.enum_type.__name__)

    def s2t(self, s: str) -> EnumSubset:
        return EnumSubset.from_string(e=self.enum_type, s=s)

    def t2s(self, t: EnumSubset) -> str:
        return t.to_string()

    def s2t_generate_from_default(self, s: str) -> EnumSubset:
        pass

    def more_help(self):
        return "allowed values {}".format(enum_type_to_list_str(self.enum_type))


class ParamChoice(Param):
    def __init__(
        self,
        help_string=NO_HELP,
        default=NO_DEFAULT,
        choice_list: List[str] = None
    ):
        super(ParamChoice, self).__init__(
            help_string=help_string,
            default=default,
            type_name="Choice",
        )
        self.choice_list = choice_list

    def s2t(self, s: str) -> Any:
        return s

    def t2s(self, t: Any) -> str:
        return t

    def more_help(self):
        return "allowed values {}".format(",".join(self.choice_list))


class ParamCreator(object):
    """
    Static namespace with all the param creation functions.
    """

    @staticmethod
    def create_int(
        help_string: str = NO_HELP,
        default: Union[int, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> int:
        """
        Create an int parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="int",
            function_s2t=convert_str_to_int,
            function_t2s=convert_int_to_str,
            function_s2t_generate_from_default=convert_str_to_int_default,
        )

    @staticmethod
    def create_list_int(
        help_string: str = NO_HELP,
        default: Union[List[int], NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> List[int]:
        """
        Create a List[int] parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="List[int]",
            function_s2t=convert_str_to_list_int,
            function_t2s=convert_list_int_to_str,
        )

    @staticmethod
    def create_list_str(
        help_string: str = NO_HELP,
        default: Union[List[str], NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> List[str]:
        """
        Create a List[str] parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="List[str]",
            function_s2t=convert_str_to_list_str,
            function_t2s=convert_list_str_to_str,
        )

    @staticmethod
    def create_int_or_none(
        help_string: str = NO_HELP,
        default: Union[int, None, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> Union[int, None]:
        """
        Create an int parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="Union[int, None]",
            function_s2t=convert_str_to_int_or_none,
            function_t2s=convert_int_or_none_to_str,
        )

    @staticmethod
    def create_str(
        help_string: str = NO_HELP,
        default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> str:
        """
        Create a string parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="str",
            function_s2t=convert_str_to_str_or_none,
            function_t2s=convert_str_or_none_to_str,
        )

    @staticmethod
    def create_str_or_none(
        help_string: str = NO_HELP,
        default: Union[str, None, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> Union[str, None]:
        """
        Create a string parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="str",
            function_s2t=convert_str_to_str,
            function_t2s=convert_str_to_str,
        )

    @staticmethod
    def create_bool(
        help_string: str = NO_HELP,
        default: Union[bool, NO_DEFAULT_TYPE] = NO_DEFAULT
    ) -> bool:
        """
        Create a bool parameter
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="bool",
            function_s2t=convert_str_to_bool,
            function_t2s=convert_bool_to_str,
        )

    @staticmethod
    def create_new_file(
        help_string: str = NO_HELP,
        default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT,
        suffixes: Union[List[str], None] = None
    ) -> str:
        """
        Create a new file parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFilename(
            help_string=help_string,
            default=default,
            type_name="new_file",
            suffixes=suffixes,
        )

    @staticmethod
    def create_existing_file(
        help_string: str = NO_HELP,
        default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT,
        suffixes: Union[List[str], None] = None
    ) -> str:
        """
        Create a new file parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFilename(
            help_string=help_string,
            default=default,
            type_name="existing_file",
            suffixes=suffixes,
        )

    @staticmethod
    def create_existing_folder(
        help_string: str = NO_HELP,
        default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT,
        suffixes: Union[List[str], None] = None,
    ) -> str:
        """
        Create a new folder parameter
        :param help_string:
        :param default:
        :param suffixes:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFilename(
            help_string=help_string,
            default=default,
            type_name="existing_folder",
            suffixes=suffixes,
        )

    @staticmethod
    def create_choice(
        choice_list: List[str],
        help_string: str = NO_HELP,
        default: Union[Any, NO_DEFAULT_TYPE] = NO_DEFAULT,
    ) -> str:
        """
        Create a choice config
        :param choice_list:
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamChoice(
            help_string=help_string,
            default=default,
            choice_list=choice_list,
        )

    @staticmethod
    def create_enum(
        enum_type: Type[Enum],
        help_string: str = NO_HELP,
        default: Union[Any, NO_DEFAULT_TYPE] = NO_DEFAULT,
    ) -> Type[Enum]:
        """
        Create an enum config
        :param enum_type:
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamEnum(
            help_string=help_string,
            default=default,
            enum_type=enum_type,
        )

    @staticmethod
    def create_enum_subset(
        enum_type: Type[Enum],
        help_string: str = NO_HELP,
        default: EnumSubset = NO_DEFAULT,
    ) -> EnumSubset:
        """
        Create an enum config
        :param enum_type:
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamEnumSubset(
            help_string=help_string,
            default=default,
            enum_type=enum_type,
        )

    @staticmethod
    def create_existing_bucket(help_string: str = NO_HELP, default: Union[str, NO_DEFAULT_TYPE] = NO_DEFAULT) -> str:
        """
        Create a bucket name on gcp
        :param help_string:
        :param default:
        :return:
        """
        # noinspection PyTypeChecker
        return ParamFunctions(
            help_string=help_string,
            default=default,
            type_name="bucket_name",
            function_s2t=convert_str_to_str,
            function_t2s=convert_str_to_str,
        )


def register_function_group(function_group_name: str, function_group_description: str) -> None:
    pt = get_pytconf()
    pt.function_group_descriptions[function_group_name] = function_group_description
    pt.function_group_list.append(function_group_name)


def register_main() -> Callable[[Any], Any]:
    def identity(f):
        get_pytconf().register_main(f)
        return f

    return identity


def register_endpoint(
    configs: List[Type[Config]] = (),
    suggest_configs: List[Type[Config]] = (),
    group: str = DEFAULT_GROUP_NAME,
    allow_free_args: bool = False,
) -> Callable[[Any], Any]:
    logger = logging.getLogger("pytconf")
    logger.debug("registering endpoint")

    def identity(f):
        register_function(
            f,
            configs=configs,
            suggest_configs=suggest_configs,
            group=group,
            allow_free_args=allow_free_args,
        )
        return f

    return identity


def register_function(
    f: Callable,
    configs: List[Type[Config]] = (),
    suggest_configs: List[Type[Config]] = (),
    group: str = DEFAULT_GROUP_NAME,
    allow_free_args: bool = False,
) -> None:
    function_name = f.__name__
    pt = get_pytconf()
    pt.function_name_to_callable[function_name] = f
    pt.function_name_to_configs[function_name] = configs
    pt.function_name_to_suggest_configs[function_name] = suggest_configs
    pt.function_group_names[group].add(function_name)
    pt.allow_free_args[function_name] = allow_free_args


def get_free_args() -> List[str]:
    return get_pytconf().free_args
