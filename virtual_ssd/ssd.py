import os
import pickle
import sys
from command_buffer.command_buffer import CommandBuffer


class SSD:
    DATA_LOC = os.path.join(os.path.dirname(__file__), "nand.txt")
    RESULT_LOC = os.path.join(os.path.dirname(__file__), "../result.txt")
    INIT_DATA = "0x00000000"
    MAX_ADDR = 100
    MAX_ERASE_SIZE = 10
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"

    def __init__(
        self,
        nand_filename: str = None,
        result_filename: str = None,
        buffer_filename: str = None,
    ):
        self.__nand_filename = nand_filename if nand_filename else SSD.DATA_LOC
        self.__result_filename = result_filename if result_filename else SSD.RESULT_LOC
        self._buffer = CommandBuffer(buffer_filename)

        if not os.path.exists(self.__nand_filename):
            self.__init_nand_file()

    def __init_nand_file(self):
        initial_data = {}
        for i in range(SSD.MAX_ADDR):
            initial_data[i] = SSD.INIT_DATA

        self.__write_nand_file(initial_data)

    def __read_nand_file(self) -> dict:
        with open(self.__nand_filename, "rb") as read_handle:
            result = pickle.loads(read_handle.read())

        return result

    def __write_result_file(self, data: str):
        with open(self.__result_filename, "w") as result_handle:
            result_handle.write(data)

    def __write_nand_file(self, dump: dict):
        with open(self.__nand_filename, "wb") as write_handle:
            pickle.dump(dump, write_handle)

    def __isvalid_address(self, addr: int):
        return type(addr) is int and 0 <= addr < self.MAX_ADDR

    def __read_nand(self, addr: int):
        read_data = self.__read_nand_file()
        self.__write_result_file(read_data[addr])

        return SSD.SUCCESS

    def __write_nand(self, addr: int, value: str):
        dump = self.__read_nand_file()

        dump[addr] = value

        self.__write_nand_file(dump)

        return SSD.SUCCESS

    def __erase_nand(self, addr: int, size: int):
        dump = self.__read_nand_file()

        for idx in range(addr, addr + size):
            dump[idx] = self.INIT_DATA

        self.__write_nand_file(dump)

        return SSD.SUCCESS

    def _process_cmd_buffer(self, buf: list):
        for cmd in buf:
            if cmd[0] == "W":
                self.__write_nand(cmd[1], cmd[2])
            elif cmd[0] == "E":
                self.__erase_nand(cmd[1], cmd[2])

    def read(self, addr: int):
        if not self.__isvalid_address(addr):
            return SSD.FAIL

        read_result = self._buffer.get_value(addr)

        if read_result is None:
            return self.__read_nand(addr)

        self.__write_result_file(read_result)
        return SSD.SUCCESS

    def write(self, addr: int, value: str):
        if not self.__isvalid_address(addr) or type(value) is not str:
            return SSD.FAIL

        buf = self._buffer.insert_cmd("W", addr, value)
        if buf is not None:
            self._process_cmd_buffer(buf)

        return SSD.SUCCESS

    def erase(self, addr: int, size: int):
        if (
            type(size) is not int
            or not 0 < size < self.MAX_ERASE_SIZE
            or not self.__isvalid_address(addr)
            or not self.__isvalid_address(addr + size)
        ):
            return SSD.FAIL

        buf = self._buffer.insert_cmd("E", addr, size)
        if buf is not None:
            self._process_cmd_buffer(buf)

        return SSD.SUCCESS


def command_runner(argv):
    if argv[1] != "ssd":
        raise Exception("WRONG COMMAND")

    ssd = SSD()
    if argv[2] == "R":
        ssd.read(int(argv[3]))
    elif argv[2] == "W":
        ssd.write(int(argv[3]), argv[4])
    elif argv[2] == "E":
        ssd.erase(int(argv[3]), int(argv[4]))
    elif argv[2] == "F":
        buf = ssd._buffer.flush()
        ssd._process_cmd_buffer(buf)


if __name__ == "__main__":
    command_runner(sys.argv)
