import sys
import os
import pickle


class SSD:
    def __init__(self):

        if not os.path.exists("nand.txt"):

            initial_data = {}
            for i in range(100):
                initial_data[i] = "0x00000000"

            with open("nand.txt", "wb") as handle:
                pickle.dump(initial_data, handle)

    def read(self, addr):
        pass

    def write(self, addr, value):
        dump = {}
        with open("nand.txt", "rb") as read_handle:
            dump = pickle.loads(read_handle.read())

        dump[addr] = value

        with open("nand.txt", "wb") as write_handle:
            pickle.dump(dump, write_handle)

        return "SUCCESS"


if __name__ == "__main__":
    print(sys.argv[0])
