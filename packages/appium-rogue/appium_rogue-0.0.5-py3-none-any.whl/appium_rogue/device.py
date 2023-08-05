# coding: utf-8
#
import abc
from PIL import Image
from . import uidumplib


class DeviceMeta(metaclass=abc.ABCMeta):
    def screenshot(self) -> Image.Image:
        pass

    def dump_hierarchy(self) -> str:
        pass

    @abc.abstractproperty
    def device(self):
        pass


class _AndroidDevice(DeviceMeta):
    def __init__(self, device_url):
        import uiautomator2 as u2
        d = u2.connect(device_url)
        self._d = d

    def screenshoot(self):
        return self._d.screenshot()

    def dump_hierarchy(self):
        return uidumplib.get_android_hierarchy(self._d)

    @property
    def device(self):
        return self._d


class _AppleDevice(DeviceMeta):
    def __init__(self, device_url):
        import wda
        c = wda.Client(device_url)
        self._client = c
        self.__scale = c.session().scale

    def screenshoot(self):
        return self._client.screenshot(format='pillow')

    def dump_hierarchy(self):
        return uidumplib.get_ios_hierarchy(self._client, self.__scale)

    @property
    def device(self):
        return self._client.session()


cached_devices = {}


def connect_device(platform, device_url):
    """
    Returns:
        deviceId (string)
    """
    device_id = platform + ":" + device_url
    if platform == 'android':
        d = _AndroidDevice(device_url)
    elif platform == 'ios':
        d = _AppleDevice(device_url)

    cached_devices[device_id] = d
    return device_id


def get_device(id):
    d = cached_devices.get(id)
    if d is None:
        platform, uri = id.split(":", maxsplit=1)
        connect_device(platform, uri)
    return cached_devices[id]
