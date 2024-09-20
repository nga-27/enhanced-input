import sys
import time
from typing import Union
from enum import Enum

from colorama import just_fix_windows_console


just_fix_windows_console()

DEFAULT_TIMEOUT = 30.0
INTERVAL = 0.05
DEFAULT_PROMPT = ""

SP = ' '
CR = '\r'
LF = '\n'
CRLF = CR + LF


class EnhancedInputColor(Enum):
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

    def __init__(self) -> None:
        try:
            import msvcrt
            self.__enhanced_input = self.__windows_input
        except ImportError:
            import selectors
            import termios
            self.__enhanced_input = self.__posix_input

    def input(self, prompt: str = DEFAULT_PROMPT,
              timeout: float = DEFAULT_TIMEOUT,
              text_color: Union[EnhancedInputColor, None] = None) -> Union[str, None]:
        """modified "input" function. Returns None on timeout or keyboard interrupt

        Args:
            prompt (str, optional): string as part of prompt. Defaults to "".
            timeout (float, optional): timeout. Defaults to DEFAULT_TIMEOUT.

        Returns:
            Union[str, None]: str of input if within timeout, None if timeout or keyboard
                            interrupt occurred
        """
        if text_color:
            prompt = f"{text_color.value}{prompt}{EnhancedInputColor.RESET.value}"
        return self.__enhanced_input(prompt=prompt, timeout=timeout)

    def __echo(self, string_val: str):
        sys.stdout.write(string_val)
        sys.stdout.flush()

    def __posix_input(self, prompt: str = DEFAULT_PROMPT,
                      timeout: float = DEFAULT_TIMEOUT) -> Union[str, None]:
        import selectors, termios
        self.__echo(prompt)
        sel = selectors.DefaultSelector()
        sel.register(sys.stdin, selectors.EVENT_READ)
        events = sel.select(timeout)

        if events:
            key, _ = events[0]
            return key.fileobj.readline().rstrip(LF)
        else:
            self.__echo(LF)
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
            return None

    def __windows_input(self, prompt: str = DEFAULT_PROMPT,
                        timeout: float = DEFAULT_TIMEOUT) -> Union[str, None]:
        import msvcrt
        self.__echo(prompt)
        begin = time.monotonic()
        end = begin + timeout
        line = ''

        while time.monotonic() < end:
            if msvcrt.kbhit():
                c = msvcrt.getwche()
                if c in (CR, LF):
                    self.__echo(CRLF)
                    return line
                if c == '\003':
                    return None
                if c == '\b':
                    line = line[:-1]
                    cover = SP * len(prompt + line + SP)
                    self.__echo(''.join([CR, cover, CR, prompt, line]))
                else:
                    line += c
            time.sleep(INTERVAL)

        self.__echo(CRLF)
        return None
