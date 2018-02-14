import serial
import unittest.mock

import pytest
import pytest_mock

import m9803r


def get_mock_serial(
        mocker: pytest_mock.MockFixture) -> unittest.mock.MagicMock:
    return mocker.patch("m9803r.serial.Serial")


def test_open_dmm(mocker: pytest_mock.MockFixture):
    expected_serial_port = "/dev/tty.usbserial"

    mock_serial_module = get_mock_serial(mocker)

    with m9803r.open_dmm():
        pass

    mock_serial_module.assert_called_once_with(
        expected_serial_port,
        bytesize=serial.SEVENBITS,
        stopbits=serial.STOPBITS_TWO)


@pytest.mark.parametrize(
    "test_bytes, expected_value",
    [
        (b"\x80\x03\x02\x00\x00\x81\x81\x80\x84\r\n", 23),  # AC Volts
        (b"\x88\x09\x05\x01\x01\x80\x80\x80\x84\r\n", 1159),  # DC Voltage
        (b"\x81\x00\x00\x00\x04\x84\x85\x80\x84\r\n", 4000),  # Resistance
        (b"\x81\x00\x00\x00\x04\x85\x80\x80\x82\r\n", 4000),  # Continuity
        (b"\x80\x00\x02\x09\x02\x86\x81\x80\x82\r\n", 2920),  # Diode
        (b"\x80\x00\x06\x01\x00\x8C\x80\x80\x84\r\n", 160),  # Capacitance
        (b"\x80\x00\x00\x00\x00\x88\x80\x80\x82\r\n", 0),  # DC Amp
        (b"\x80\x03\x00\x00\x00\x89\x80\x80\x82\r\n", 3),  # AC Amp
        (b"\x80\x00\x00\x00\x00\x82\x82\x80\x82\r\n", 0),  # DC mA
        (b"\x80\x04\x00\x00\x00\x83\x82\x80\x82\r\n", 4),  # AC mA
        (b"\x80\x00\x00\x00\x00\x87\x80\x80\x82\r\n", 0),  # ADP
        (b"\x80\x04\x07\x09\x01\x8a\x80\x80\x84\r\n", 1974)  # Frequency
    ])
def test_get_digits(test_bytes: bytes, expected_value: int,
                    mocker: pytest_mock.MockFixture):

    result = m9803r.Sample._get_digits(test_bytes[1:5])
    assert result == expected_value


@pytest.mark.parametrize(
    "test_bytes, expected_value",
    [
        (b"\x80\x03\x02\x00\x00\x81\x81\x80\x84\r\n", False),  # AC Volts
        (b"\x88\x09\x05\x01\x01\x80\x80\x80\x84\r\n", True),  # DC Voltage
        (b"\x81\x00\x00\x00\x04\x84\x85\x80\x84\r\n", False),  # Resistance
        (b"\x81\x00\x00\x00\x04\x85\x80\x80\x82\r\n", False),  # Continuity
        (b"\x80\x00\x02\x09\x02\x86\x81\x80\x82\r\n", False),  # Diode
        (b"\x80\x00\x06\x01\x00\x8C\x80\x80\x84\r\n", False),  # Capacitance
        (b"\x80\x00\x00\x00\x00\x88\x80\x80\x82\r\n", False),  # DC Amp
        (b"\x80\x03\x00\x00\x00\x89\x80\x80\x82\r\n", False),  # AC Amp
        (b"\x80\x00\x00\x00\x00\x82\x82\x80\x82\r\n", False),  # DC mA
        (b"\x80\x04\x00\x00\x00\x83\x82\x80\x82\r\n", False),  # AC mA
        (b"\x80\x00\x00\x00\x00\x87\x80\x80\x82\r\n", False),  # ADP
        (b"\x80\x04\x07\x09\x01\x8a\x80\x80\x84\r\n", False)  # Frequency
    ])
def test_get_is_negative(test_bytes: bytes, expected_value: int,
                         mocker: pytest_mock.MockFixture):

    result = m9803r.Sample._get_is_negative(test_bytes[0])
    assert result == expected_value


@pytest.mark.parametrize(
    "test_bytes, expected_value",
    [
        (b"\x80\x03\x02\x00\x00\x81\x81\x80\x84\r\n", False),  # AC Volts
        (b"\x88\x09\x05\x01\x01\x80\x80\x80\x84\r\n", False),  # DC Voltage
        (b"\x81\x00\x00\x00\x04\x84\x85\x80\x84\r\n", True),  # Resistance
        (b"\x81\x00\x00\x00\x04\x85\x80\x80\x82\r\n", True),  # Continuity
        (b"\x80\x00\x02\x09\x02\x86\x81\x80\x82\r\n", False),  # Diode
        (b"\x80\x00\x06\x01\x00\x8C\x80\x80\x84\r\n", False),  # Capacitance
        (b"\x80\x00\x00\x00\x00\x88\x80\x80\x82\r\n", False),  # DC Amp
        (b"\x80\x03\x00\x00\x00\x89\x80\x80\x82\r\n", False),  # AC Amp
        (b"\x80\x00\x00\x00\x00\x82\x82\x80\x82\r\n", False),  # DC mA
        (b"\x80\x04\x00\x00\x00\x83\x82\x80\x82\r\n", False),  # AC mA
        (b"\x80\x00\x00\x00\x00\x87\x80\x80\x82\r\n", False),  # ADP
        (b"\x80\x04\x07\x09\x01\x8a\x80\x80\x84\r\n", False)  # Frequency
    ])
def test_get_is_overload(test_bytes: bytes, expected_value: int,
                         mocker: pytest_mock.MockFixture):

    result = m9803r.Sample._get_is_overload(test_bytes[0])
    assert result == expected_value


@pytest.mark.parametrize(
    "test_bytes, expected_value",
    [
        (b"\x80\x03\x02\x00\x00\x81\x81\x80\x84\r\n",
         m9803r.Mode.AC_V),  # AC Volts
        (b"\x88\x09\x05\x01\x01\x80\x80\x80\x84\r\n",
         m9803r.Mode.DC_V),  # DC Voltage
        (b"\x81\x00\x00\x00\x04\x84\x85\x80\x84\r\n",
         m9803r.Mode.OHM),  # Resistance
        (b"\x81\x00\x00\x00\x04\x85\x80\x80\x82\r\n",
         m9803r.Mode.CONTINUITY),  # Continuity
        (b"\x80\x00\x02\x09\x02\x86\x81\x80\x82\r\n",
         m9803r.Mode.DIODE),  # Diode
        (b"\x80\x00\x06\x01\x00\x8C\x80\x80\x84\r\n",
         m9803r.Mode.CAP),  # Capacitance
        (b"\x80\x00\x00\x00\x00\x88\x80\x80\x82\r\n",
         m9803r.Mode.DC_A),  # DC Amp
        (b"\x80\x03\x00\x00\x00\x89\x80\x80\x82\r\n",
         m9803r.Mode.AC_A),  # AC Amp
        (b"\x80\x00\x00\x00\x00\x82\x82\x80\x82\r\n",
         m9803r.Mode.DC_MA),  # DC mA
        (b"\x80\x04\x00\x00\x00\x83\x82\x80\x82\r\n",
         m9803r.Mode.AC_MA),  # AC mA
        (b"\x80\x00\x00\x00\x00\x87\x80\x80\x82\r\n", m9803r.Mode.ADP),  # ADP
        (b"\x80\x04\x07\x09\x01\x8a\x80\x80\x84\r\n",
         m9803r.Mode.FREQ),  # Frequency
    ])
def test_get_mode(test_bytes: bytes, expected_value: int,
                  mocker: pytest_mock.MockFixture):

    result = m9803r.Sample._get_mode(test_bytes[5])
    assert result == expected_value
