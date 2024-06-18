import os
import pickle

class SSD:
    DATA_LOC = "../nand.txt"
    DATA_READ = "../result.txt"
    INIT_DATA = "0x00000000"
    MAX_ADDR = 100
    WRITE_SUCCESS = "SUCCESS"
    READ_SUCCESS = "SUCCESS"

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
        try:
            with open(SSD.DATA_LOC, "rb") as handle:
                read_data = pickle.load(handle)

            with open(SSD.DATA_READ, 'w') as result_file:
                result_file.write(read_data[addr])
                result_file.close()

            return SSD.READ_SUCCESS
        except:
            if os.path.isfile(SSD.DATA_READ):
                os.remove(SSD.DATA_READ)

    def write(self, addr, value):
        dump = {}

        with open(SSD.DATA_LOC, "rb") as read_handle:
            dump = pickle.loads(read_handle.read())

        dump[addr] = value

        with open(SSD.DATA_LOC, "wb") as write_handle:
            pickle.dump(dump, write_handle)

        return SSD.WRITE_SUCCESS
