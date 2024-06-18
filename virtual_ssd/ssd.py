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

    def __init__(self):
        if not os.path.exists(SSD.DATA_LOC):
            self.init_nand()

    def init_nand(self):
        initial_data = {}
        for i in range(SSD.MAX_ADDR):
            initial_data[i] = SSD.INIT_DATA

        with open(SSD.DATA_LOC, "wb") as handle:
            pickle.dump(initial_data, handle)

    def __read_nand(self) -> dict:
        with open(SSD.DATA_LOC, "rb") as read_handle:
            result = pickle.loads(read_handle.read())

        return result

    def __write_result_file(self, data: str):
        with open(SSD.DATA_READ, "w") as result_handle:
            result_handle.write(data)

    def read(self, addr: int):
        try:
            read_data = self.__read_nand()
            self.__write_result_file(read_data[addr])

            return SSD.SUCCESS
        except:
            if os.path.isfile(SSD.DATA_READ):
                os.remove(SSD.DATA_READ)

            return SSD.FAIL

    def write(self, addr: int, value: str):
        dump = self.__read_nand()

        if type(value) is not str:
            return SSD.FAIL

        dump = {}

        with open(SSD.DATA_LOC, "rb") as read_handle:
            dump = pickle.loads(read_handle.read())

        dump[addr] = value

        with open(SSD.DATA_LOC, "wb") as write_handle:
            pickle.dump(dump, write_handle)

        return SSD.SUCCESS


def main(argv):
    if argv[1] != "ssd":
        raise Exception("WRONG COMMAND")

    ssd = SSD()
    if argv[2] == "R":
        ssd.read(argv[3])
    elif argv[2] == "W":
        ssd.write(argv[3], argv[4])


if __name__ == "__main__":
    main(sys.argv)
