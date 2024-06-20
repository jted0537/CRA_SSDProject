import os
import pickle
import sys


class SSD:
    DATA_LOC = os.path.join(os.path.dirname(__file__), "nand.txt")
    RESULT_LOC = os.path.join(os.path.dirname(__file__), "../result.txt")
    INIT_DATA = "0x00000000"
    MAX_ADDR = 100
    MAX_ERASE_SIZE = 10
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"

    def __init__(self, nand_filename: str = None, result_filename: str = None):
        self.__nand_filename = nand_filename if nand_filename else SSD.DATA_LOC
        self.__result_filename = result_filename if result_filename else SSD.RESULT_LOC

        if not os.path.exists(self.__nand_filename):
            self.init_nand()

    def init_nand(self):
        initial_data = {}
        for i in range(SSD.MAX_ADDR):
            initial_data[i] = SSD.INIT_DATA

        with open(self.__nand_filename, "wb") as handle:
            pickle.dump(initial_data, handle)

    def __read_nand(self) -> dict:
        with open(self.__nand_filename, "rb") as read_handle:
            result = pickle.loads(read_handle.read())

        return result

    def __write_result_file(self, data: str):
        with open(self.__result_filename, "w") as result_handle:
            result_handle.write(data)

    def __write_nand_file(self, dump: dict):
        with open(self.__nand_filename, "wb") as write_handle:
            pickle.dump(dump, write_handle)

    def _isvalid_address(self, addr: int):
        return type(addr) is int and 0 < addr < self.MAX_ADDR

    def read(self, addr: int):
        if not self._isvalid_address(addr):
            return SSD.FAIL

        try:
            read_data = self.__read_nand()
            self.__write_result_file(read_data[addr])

            return SSD.SUCCESS
        except:
            if os.path.isfile(self.__result_filename):
                os.remove(self.__result_filename)

            return SSD.FAIL

    def write(self, addr: int, value: str):
        if not self._isvalid_address(addr) or type(value) is not str:
            return SSD.FAIL

        dump = self.__read_nand()

        dump[addr] = value

        self.__write_nand_file(dump)

        return SSD.SUCCESS

    def erase(self, addr: int, size: int):
        if not self._isvalid_address(addr) or type(size) is not int:
            return SSD.FAIL
        if size < 0 or size > self.MAX_ERASE_SIZE or addr + size > self.MAX_ADDR:
            return SSD.FAIL

        dump = self.__read_nand()

        for idx in range(addr, addr + size):
            dump[idx] = self.INIT_DATA

        self.__write_nand_file(dump)

        return SSD.SUCCESS


def main(argv):
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
        pass


if __name__ == "__main__":
    main(sys.argv)
