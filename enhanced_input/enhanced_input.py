""" Single only file that handles the enhanced input """
import sys
import time
import platform
from typing import Union
from enum import Enum

import maskpass
from colorama import just_fix_windows_console # pylint: disable=import-error


just_fix_windows_console()

DEFAULT_TIMEOUT = 30.0
INTERVAL = 0.05
DEFAULT_PROMPT = ""

SP = ' '
CR = '\r'
LF = '\n'
CRLF = CR + LF


class EnhancedInputColor(Enum):
    """ Colorama and EnhancedInput-supported color mappings """
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"


class EnhancedInput:
    """ Class that handles enhanced '.input()' functionality """
    # pylint: disable=too-few-public-methods

    def __init__(self) -> None:
        """ This seemed the best way to determine """
        if 'windows' in platform.system().lower():
            self.__enhanced_input = self.__windows_input
        else:
            self.__enhanced_input = self.__posix_input

    def input(self, prompt: str = DEFAULT_PROMPT,
              timeout: float = DEFAULT_TIMEOUT,
              text_color: Union[EnhancedInputColor, None] = None,
              password_mask: Union[str, None] = None) -> Union[str, None]:
        """modified "input" function. Returns None on timeout or keyboard interrupt

        Args:
            prompt (str, optional): string as part of prompt. Defaults to "".
            timeout (float, optional): timeout. Defaults to DEFAULT_TIMEOUT.
            text_color (EnhancedInputColor, optional): text color. Defaults to None.
            password_mask (str, optional): if None, will be normal input. If str (even empty
                                            string), will do a maskpass password. Default is None. 

        Returns:
            Union[str, None]: str of input if within timeout, None if timeout or keyboard
                            interrupt occurred
        """
        if text_color:
            prompt = f"{text_color.value}{prompt}{EnhancedInputColor.RESET.value}"
        if password_mask is not None:
            return maskpass.askpass(mask=password_mask, prompt=prompt)
        return self.__enhanced_input(prompt=prompt, timeout=timeout)

    def __echo(self, string_val: str):
        sys.stdout.write(string_val)
        sys.stdout.flush()

    def __posix_input(self, prompt: str = DEFAULT_PROMPT,
                      timeout: float = DEFAULT_TIMEOUT) -> Union[str, None]:
        import selectors # pylint: disable=import-outside-toplevel,import-error
        import termios # pylint: disable=import-outside-toplevel,import-error
        self.__echo(prompt)
        sel = selectors.DefaultSelector()
        sel.register(sys.stdin, selectors.EVENT_READ)
        events = sel.select(timeout)

        if events:
            key, _ = events[0]
            return key.fileobj.readline().rstrip(LF)
        self.__echo(LF)
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        return None

    def __windows_input(self, prompt: str = DEFAULT_PROMPT,
                        timeout: float = DEFAULT_TIMEOUT) -> Union[str, None]:
        import msvcrt # pylint: disable=import-outside-toplevel,import-error
        self.__echo(prompt)
        begin = time.monotonic()
        end = begin + timeout
        line = ''

        while time.monotonic() < end:
            if msvcrt.kbhit():
                char_val = msvcrt.getwche()
                if char_val in (CR, LF):
                    self.__echo(CRLF)
                    return line
                if char_val == '\003':
                    return None
                if char_val == '\b':
                    line = line[:-1]
                    cover = SP * len(prompt + line + SP)
                    self.__echo(''.join([CR, cover, CR, prompt, line]))
                else:
                    line += char_val
            time.sleep(INTERVAL)

        self.__echo(CRLF)
        return None
