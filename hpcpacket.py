from abc import abstractmethod
from struct import pack

class HPCPacket:
    _PACKET_START = 0x3e
    _PACKET_END = 0x3c

    def __init__(self, packet_type: int) -> None:
        self._type = packet_type

    @abstractmethod
    def get_data(self) -> list[int]:
        raise NotImplementedError()

    def get_bytes(self) -> bytes:
        data = list(pack("<h", self._type)) + self.get_data()
        result = [
            self._PACKET_START
        ] + data + [
            self.crc(data),
            self._PACKET_END
        ]
        return bytes(result)

    @staticmethod
    def crc(data: list[int]) -> int:
        result = 0
        for i in data:
            result += i
        return result


