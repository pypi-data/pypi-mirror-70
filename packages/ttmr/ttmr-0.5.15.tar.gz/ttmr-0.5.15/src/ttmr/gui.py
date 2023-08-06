import platform
from time import sleep
from plyer import notification
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion
from prompt_toolkit.validation import ValidationError
from prompt_toolkit.validation import Validator
from tabulate import tabulate
from ttmr.time import Date
from ttmr.time import Alarm
from .console import BG_WHITE
from .console import BLACK
from .console import RED
from .console import Console
from .time import Timer
from .util import DefaultFormatter
from .util import add_table_border

if platform.system() == "Windows":
    import msvcrt  # pylint: disable=E0401


def display_alert(message):
    Console.write(RED)
    Console.writeline(message)
    Console.clear_formating()


def display_message(message):
    Console.clear_formating()
    Console.write(message)
    Console.newline()


def clear_line():
    Console.cursor_to_left_margin()
    Console.clear_line()


class ObjectCompleter(Completer):
    def __init__(self, objects):

        self.objects = objects

    def get_completions(self, document, complete_event):

        word_before_cursor = document.get_word_before_cursor(WORD=False)
        word_before_cursor = word_before_cursor.lower()

        for o in self.objects:
            if o.name.lower().startswith(word_before_cursor):
                yield Completion(
                    o.name, -len(word_before_cursor), display_meta=str(o.id)
                )


def format_prompt_msg(msg, min_len=10):
    _len = len(msg) if len(msg) > min_len else min_len
    INPUT_REQUEST_FMT = f"{{: >{_len}}}: "
    return INPUT_REQUEST_FMT.format(msg)


def promptor(func):
    """Prompt decorator that provides a common format
    to a prompts query.

    """

    def _promptor(input_query, *args, **kwargs):
        query = format_prompt_msg(input_query)
        return func(query, *args, **kwargs)

    return _promptor


@promptor
def text_input(input_query, default=None):
    prompt_opt = {}
    if default:
        prompt_opt["default"] = default
    return prompt(input_query, **prompt_opt)


class OptionValidator(Validator):
    def __init__(self, options):
        super(OptionValidator, self).__init__()
        self.options = options

    def validate(self, document):
        if document.text not in self.options:
            raise ValidationError(message="Must select complete row", cursor_position=0)


@promptor
def option_input(input_query, options, default=None):
    option_dict = {e.name: e for e in options}
    prompt_opt = {
        "completer": ObjectCompleter(options),
        "validator": OptionValidator(option_dict),
    }
    prompt_opt["default"] = "" if default is None else str(default)
    text = prompt(input_query, **prompt_opt)
    return option_dict.get(text, text)


class NumberValidator(Validator):
    def __init__(self, default, *args, **kwargs):
        super(NumberValidator, self).__init__(*args, **kwargs)
        self.translated_value = default

    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(
                message="Duration must be a number!", cursor_position=i
            )

        self.translated_value = int(text) if text else 0


@promptor
def default_text_input(input_query, default):
    return prompt(input_query, default=default)


@promptor
def number_input(input_query, default):
    validator = NumberValidator(0)
    prompt(input_query, default=default, validator=validator)
    return validator.translated_value


@promptor
def duration_input(input_query, default=0):
    validator = NumberValidator(0)
    prompt(input_query, default=default, validator=validator)
    return validator.translated_value


class DateValidator(Validator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.translated_value = None

    def translate(self, input_value):
        try:
            self.translated_value = Date.parse(input_value)  # , "%Y-%m-%d %H:%M:%S")
        except Exception as ex:
            raise ValidationError(message=ex)

    def validate(self, document):
        self.translate(document.text)


@promptor
def date_input(input_query, default=None):
    validator = DateValidator()
    if not default:
        display_value = Date.current().strftime("%Y-%m-%d %H:%M")
    else:
        display_value = default.strftime("%Y-%m-%d %H:%M")
    prompt(
        input_query,
        default=display_value,
        validator=validator,
        validate_while_typing=False,
    )
    return validator.translated_value


class BooleanValidator(Validator):
    def __init__(self, *args, **kwargs):
        super(BooleanValidator, self).__init__(*args, **kwargs)
        self.translated_value = False
        self.true_str = ("y", "yes", "true", "1")
        self.false_str = ("n", "no", "false", "0")

    def parse(self, input_value):
        if input_value in self.true_str:
            return True
        if input_value in self.false_str:
            return False
        raise ValidationError(message="Must enter valid reply.", cursor_position=0)

    def validate(self, document):
        self.translated_value = self.parse(document.text.lower())


@promptor
def bool_input(input_query):
    validator = BooleanValidator()
    prompt(input_query, validator=validator)
    return validator.translated_value


def write_table(data, headers, formaters=None):
    Console.write(BG_WHITE)
    Console.write(BLACK)
    Console.newline()

    fmt = DefaultFormatter()

    if formaters:
        if len(headers) != len(formaters):
            raise Exception("The number of headers and formaters do not match!")
        _data = []
        for row in data:
            _data.append(
                [
                    fmt.format(formaters[i], c) if formaters[i] else c
                    for i, c in enumerate(row)
                ]
            )

        data = _data

    table = tabulate(data, headers=headers, numalign="decimal")

    Console.write(add_table_border(table))

    Console.newline()
    Console.clear_formating()

    data.insert(0, headers)
    return data


def show_timer(start_time, alarms=None):
    """show_timer displays a timer incrementing clock in
    a HH:MM:SS format for the given start_time.

    The timer will continuously increment until the console
    registers a keyboard press.

    """
    DSPLY_FMT = " {: >10}: {}  \n\n"
    timer = Timer(start_time, alarms)

    def write_display():
        Console.write(DSPLY_FMT.format("Timer", timer.get_formatted_lapsed_time()))
        timer.check_alarms()

    write_display()

    while True:
        sleep(1)
        Console.cursor_up()
        Console.cursor_up()
        Console.cursor_to_left_margin()
        Console.clear_line()
        write_display()
        # this only works on Windows.
        if platform.system() == "Windows":
            # kbhit returns True if the keyboard is struck.
            if msvcrt.kbhit():
                break
