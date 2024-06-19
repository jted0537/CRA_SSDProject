import os
import pickle
import sys


class SSD:
    DATA_LOC = "../nand.txt"
    DATA_READ = "../result.txt"
    INIT_DATA = "0x00000000"
    MAX_ADDR = 100
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"

    def __init__(self, nand_filename: str = None, result_filename: str = None):

        self.__nand_filename = nand_filename if nand_filename else SSD.DATA_LOC
        self.__result_filename = result_filename if result_filename else SSD.DATA_READ

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

    def read(self, addr: int):
        try:
            read_data = self.__read_nand()
            self.__write_result_file(read_data[addr])

            return SSD.SUCCESS
        except:
            if os.path.isfile(self.__result_filename):
                os.remove(self.__result_filename)

            return SSD.FAIL

    def write(self, addr: int, value: str):

        if type(value) is not str:
            return SSD.FAIL

        dump = self.__read_nand()

        dump[addr] = value

        with open(self.__nand_filename, "wb") as write_handle:
            pickle.dump(dump, write_handle)

        return SSD.SUCCESS


def main(argv):
    if argv[1] != "ssd":
        raise Exception("WRONG COMMAND")

    ssd = SSD()
    if argv[2] == "R":
        ssd.read(int(argv[3]))
    elif argv[2] == "W":
        ssd.write(int(argv[3]), argv[4])


if __name__ == "__main__":
    main(sys.argv)
