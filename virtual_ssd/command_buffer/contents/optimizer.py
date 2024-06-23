import copy
import abc


class Optimizer(abc.ABC):
    def _traverse_and_optimize(self, command_buffer: list, compare_function: callable):
        should_delete = [False] * len(command_buffer)

        for i in range(len(command_buffer) - 1, -1, -1):
            content_i = command_buffer[i]

            for j in range(0, i):
                content_j = command_buffer[j]

                if compare_function(content_i, content_j):
                    should_delete[j] = True

        optimized_buffer = copy.copy(command_buffer)

        for i in range(len(command_buffer) - 1, -1, -1):
            if should_delete[i]:
                del optimized_buffer[i]

        return optimized_buffer

    @abc.abstractmethod
    def optimize(self, command_buffer: list):
        raise NotImplementedError


class ReduceWriteDuplication(Optimizer):
    def __compare_function(self, content_i, content_j):
        if content_i[0] == "W" and content_j[0] == "W" and content_i[1] == content_j[1]:
            return True

        return False

    def optimize(self, command_buffer: list):
        return self._traverse_and_optimize(command_buffer, self.__compare_function)


class ReduceWriteByErase(Optimizer):
    def __compare_function(self, content_i, content_j):
        if (
            content_i[0] == "E"
            and content_j[0] == "W"
            and content_i[1] <= content_j[1] < content_i[1] + content_i[2]
        ):
            return True

        return False

    def optimize(self, command_buffer: list):
        return self._traverse_and_optimize(command_buffer, self.__compare_function)
