class Shell:
    def __init__(self):
        self._lbas = [0] * 100

    def write(self, addr, val):
        pass

    def read(self, addr):
        pass

    def exit(self):
        pass

    def help(self):
        pass

    def full_write(self, val):
        for addr in range(100):
            self.write(addr, val)

    def full_read(self):
        pass
