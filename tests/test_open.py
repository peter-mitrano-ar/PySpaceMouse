from unittest.mock import patch
import pytest
import pyspacemouse
from pathlib import Path

# We mock the HID class from easyhid, since it only supports constructing from C data structures
class HIDDevice:
    def __init__(self, interface_number: int,
                 manufacturer_string: str,
                 path: str,
                 product_id: int,
                 product_string: str,
                 release_number: int,
                 serial_number: str,
                 usage: int,
                 usage_page: int,
                 vendor_id: int):
        self.interface_number = interface_number
        self.manufacturer_string = manufacturer_string
        self.path = path
        self.product_id = product_id
        self.product_string = product_string
        self.release_number = release_number
        self.serial_number = serial_number
        self.usage = usage
        self.usage_page = usage_page
        self.vendor_id = vendor_id

    def open(self):
        pass

    def set_nonblocking(self, nonblocking: bool):
        pass

class Enumeration:
    def __init__(self, device_list):
        self.device_list = device_list


# These three HID devices toegether represent one SpaceMouse Wireless BT device
MOCK_WIRELESS_BT_1 = HIDDevice(
    interface_number=0,
    manufacturer_string='3Dconnexion',
    path='/dev/hidraw1',
    product_id=50746,
    product_string='SpaceMouse Wireless BT',
    release_number=1284,
    serial_number='',
    usage=8,
    usage_page=1,
    vendor_id=9583
)

MOCK_WIRELESS_BT_2 = HIDDevice(
    interface_number=0,
    manufacturer_string='3Dconnexion',
    path='/dev/hidraw1',
    product_string='SpaceMouse Wireless BT',
    product_id=50746,
    release_number=1284,
    serial_number='',
    usage=58,
    usage_page=65280,
    vendor_id=9583
)

MOCK_WIRELESS_BT_3 = HIDDevice(
    interface_number=0,
    manufacturer_string='3Dconnexion',
    path='/dev/hidraw1',
    product_string='SpaceMouse Wireless BT',
    product_id=50746,
    release_number=1284,
    serial_number='',
    usage=1,
    usage_page=65280,
    vendor_id=9583
)

MOCK_HID_ENUMERATION = Enumeration(device_list=[MOCK_WIRELESS_BT_1, MOCK_WIRELESS_BT_2, MOCK_WIRELESS_BT_3])


def test_open_no_args():
    with patch("pyspacemouse.pyspacemouse.hid_enumeration", lambda: MOCK_HID_ENUMERATION):
        d = pyspacemouse.open()
        assert d is not None

def test_open_with_device_ane_path(mocker):
    with patch("pyspacemouse.pyspacemouse.hid_enumeration", lambda: MOCK_HID_ENUMERATION):
        mocker.patch("pathlib.Path.exists", return_value=True)
        d = pyspacemouse.open(device="SpaceMouse Wireless BT", path="/dev/hidraw1")
        assert d is not None

def test_open_with_device_and_missing_path():
    with patch("pyspacemouse.pyspacemouse.hid_enumeration", lambda: MOCK_HID_ENUMERATION):
        with pytest.raises(FileNotFoundError):
            d = pyspacemouse.open(device="SpaceMouse Wireless BT", path="/dev/hidraw-missing")
            assert d is not None
