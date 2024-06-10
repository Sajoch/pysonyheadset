from enum import auto, Enum
from typing import Optional

import bluetooth

from hpcpacket import HPCPacket

_UUIDS = [
    "956C7B26-D49A-4BA8-B03F-B17D393CB6E2",
    "96cc203e-5068-46ad-b32d-e316f5e069ba",
    "ba69e0f5-16e3-2db3-ad46-68503e20cc96" 
]

class ANCMode(Enum):
    DISABLE = auto()
    NOISE_CANCELLING = auto()
    AMBIENT_SOUND = auto()


class SonyHeadset:
    def __init__(self, bt_addr: str) -> None:
        self._bt_addr = bt_addr
        self._socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def connect(self) -> None:
        service = self._get_service()
        host = service["host"]
        port = service["port"]
        self._socket.connect((host, port))

    def disconnect(self) -> None:
        self._socket.close()

    def set_noise_cancellation(self, mode: ANCMode) -> None:
        packet = ANCPacket(mode)
        self._socket.send(packet.get_bytes())

    def _get_service(self) -> Optional[dict]:
        services = bluetooth.find_service(address=self._bt_addr)
        for service in services:
            service_uuids = service["service-classes"]
            if len(set(_UUIDS).intersection(service_uuids)) == 0:
                continue
            return service

        return None

class ANCPacket(HPCPacket):
    _MAGIC_HEADER = [0x00, 0x00, 0x00, 0x08, 0x68, 0x15, 0x01]

    def __init__(self, mode: ANCMode) -> None:
        super().__init__(0x000C)
        self._noise_cancelling = mode != ANCMode.DISABLE
        self._voice_passthrough = mode == ANCMode.AMBIENT_SOUND
        self._ambient = mode == ANCMode.AMBIENT_SOUND
        self._mode = self._get_mode(mode)
        self._wind_cancelling = True
        self._volume = 20


    def get_data(self) -> list[int]:
        return self._MAGIC_HEADER + [
            0x01 if self._noise_cancelling else 0x00,
            0x01 if self._ambient else 0x00,
            self._mode,
            0x01 if self._voice_passthrough else 0x00,
            self._volume, # VOLUME(1-20) -> 0x01 - 0x14
        ]

    @staticmethod
    def _get_mode(mode: ANCMode) -> int:
        if mode == ANCMode.NOISE_CANCELLING:
            return 0x02
        # elif mode == ANCMode.NOISE_WIND_CANCELLING: return 0x03
        elif mode == ANCMode.AMBIENT_SOUND:
            return 0x05
