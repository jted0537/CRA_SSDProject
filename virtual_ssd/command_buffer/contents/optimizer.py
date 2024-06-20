import copy
import abc


class Optimizer(abc.ABC):
    @abc.abstractmethod
    def optimize(self, command_buffer: list):
        raise NotImplementedError


class ReduceWriteDuplication(Optimizer):
    def optimize(self, command_buffer: list):
        should_delete = [False] * len(command_buffer)

        for i in range(len(command_buffer) - 1, -1, -1):
            cmd_i, arg1_i, arg2_i = command_buffer[i]

            if cmd_i != "W":
                continue

            for j in range(0, i):
                cmd_j, arg1_j, arg2_j = command_buffer[j]

                if cmd_i == "W" and cmd_j == "W" and arg1_i == arg1_j:
                    should_delete[j] = True

        optimized_buffer = copy.copy(command_buffer)

        for i in range(len(command_buffer) - 1, -1, -1):
            if should_delete[i]:
                del optimized_buffer[i]

        return optimized_buffer


class ReduceWriteByErase(Optimizer):
    def optimize(self, command_buffer: list):
        should_delete = [False] * len(command_buffer)

        for i in range(len(command_buffer) - 1, -1, -1):
            cmd_i, arg1_i, arg2_i = command_buffer[i]

            if cmd_i != "E":
                continue

            for j in range(0, i):
                cmd_j, arg1_j, arg2_j = command_buffer[j]

                if cmd_j == "W" and arg1_i <= arg1_j < arg1_i + arg2_i:
                    should_delete[j] = True

        optimized_buffer = copy.copy(command_buffer)

        for i in range(len(command_buffer) - 1, -1, -1):
            if should_delete[i]:
                del optimized_buffer[i]

        return optimized_buffer
