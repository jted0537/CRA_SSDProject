import sys
import os
import pickle


class SSD:
    DATA_LOC = "../nand.txt"
    INIT_DATA = "0x00000000"
    MAX_ADDR = 100
    WRITE_SUCCESS = "SUCCESS"

    def __init__(self):
        if not os.path.exists(SSD.DATA_LOC):
            self.init_nand()

    def init_nand(self):
        initial_data = {}
        for i in range(SSD.MAX_ADDR):
            initial_data[i] = SSD.INIT_DATA

        with open(SSD.DATA_LOC, "wb") as handle:
            pickle.dump(initial_data, handle)

    def read(self, addr):
        pass

    def write(self, addr, value):
        dump = {}

        with open(SSD.DATA_LOC, "rb") as read_handle:
            dump = pickle.loads(read_handle.read())

        dump[addr] = value

        with open(SSD.DATA_LOC, "wb") as write_handle:
            pickle.dump(dump, write_handle)

        return SSD.WRITE_SUCCESS


if __name__ == "__main__":
    print(sys.argv[0])
