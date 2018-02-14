import contextlib
import enum

import serial


class Mode(enum.Enum):
    DC_V = 0
    AC_V = 1
    DC_MA = 2
    AC_MA = 3
    OHM = 4
    CONTINUITY = 5
    DIODE = 6
    ADP = 7
    DC_A = 8
    AC_A = 9
    FREQ = 10
    CAP = 12


_BYTE_MASK = 0x7F


class Sample(object):
    def __init__(self, sample: bytes):
        self._data = sample
        self._parse_message()

    def _parse_message(self):
        pass

    @staticmethod
    def _get_digits(digit_data: bytes) -> int:
        """Takes bytes[1:5]"""
        result = 0
        multiplier = 1
        for digit in digit_data:
            result += multiplier * digit
            multiplier *= 10

        return result

    @staticmethod
    def _get_is_negative(digit_data: int) -> bool:
        """Takes bytes[0]"""
        NEGATIVE_MASK = 0x08
        return bool(NEGATIVE_MASK & digit_data)

    @staticmethod
    def _get_is_overload(digit_data: int) -> bool:
        """Takes bytes[0]"""
        OVERLOAD_MASK = 0x01
        return bool(OVERLOAD_MASK & digit_data)

    @staticmethod
    def _get_mode(digit_data: int) -> Mode:
        """Takes bytes[5]"""
        return Mode(digit_data)


@contextlib.contextmanager
def open_dmm() -> serial.Serial:
    port = serial.Serial(
        "/dev/tty.usbserial",
        bytesize=serial.SEVENBITS,
        stopbits=serial.STOPBITS_TWO)
    yield port
    port.close()


def main():
    with open_dmm() as port:
        print("{0.baudrate},{0.bytesize},{0.parity},{0.stopbits}".format(port))
        while True:
            print(port.readline())


if __name__ == '__main__':
    main()
