import copy
import abc


class Optimizer(abc.ABC):
    def _traverse_and_optimize(
        self, command_buffer: list, compare_optimize_function: callable
    ):
        should_delete = [False] * len(command_buffer)

        for i in range(len(command_buffer) - 1, -1, -1):
            for j in range(0, i):
                if compare_optimize_function(command_buffer, i, j):
                    should_delete[j] = True

        return self.__remove_redundancy(command_buffer, should_delete)

    def _optimize_adjacent(
        self, command_buffer: list, compare_optimize_function: callable
    ):
        should_delete = [False] * len(command_buffer)

        for i in range(len(command_buffer) - 1, 0, -1):

            if compare_optimize_function(command_buffer, i, i - 1):
                should_delete[i - 1] = True
                should_delete[i] = False
                # The optimized element of [i] should not be deleted,
                # even if it is used by prior optimization phase

        return self.__remove_redundancy(command_buffer, should_delete)

    def __remove_redundancy(self, command_buffer: list, remove_map: list):
        optimized_buffer = copy.copy(command_buffer)

        for i in range(len(command_buffer) - 1, -1, -1):
            if remove_map[i]:
                del optimized_buffer[i]

        return optimized_buffer

    @abc.abstractmethod
    def optimize(self, command_buffer: list):
        raise NotImplementedError


class ReduceWriteDuplication(Optimizer):
    def __compare_function(self, contents: list, i: int, j: int):
        if (
            contents[i][0] == "W"
            and contents[j][0] == "W"
            and contents[i][1] == contents[j][1]
        ):
            return True

        return False

    def optimize(self, command_buffer: list):
        return self._traverse_and_optimize(command_buffer, self.__compare_function)


class ReduceWriteByErase(Optimizer):
    def __compare_function(self, contents: list, i: int, j: int):
        if (
            contents[i][0] == "E"
            and contents[j][0] == "W"
            and contents[i][1] <= contents[j][1] < contents[i][1] + contents[i][2]
        ):
            return True

        return False

    def optimize(self, command_buffer: list):
        return self._traverse_and_optimize(command_buffer, self.__compare_function)


class ReduceEraseDuplication(Optimizer):
    def __compare_function(self, contents: list, i: int, j: int):
        if (
            contents[i][0] == "E"
            and contents[j][0] == "E"
            and contents[i][1] <= contents[j][1]
            and contents[j][1] + contents[j][2] <= contents[i][1] + contents[i][2]
        ):
            return True

        return False

    def optimize(self, command_buffer: list):
        return self._traverse_and_optimize(command_buffer, self.__compare_function)


class MergeAdjacentErase(Optimizer):
    def __compare_optimize_function(self, contents: list, i: int, j: int):

        if contents[i][0] != "E" or contents[j][0] != "E":
            return False

        left = contents[j][1]
        right = contents[i][1] + contents[i][2]
        overlapped = contents[i][1] - 1 <= contents[j][1] + contents[j][2]
        merged_erase_size = right - left

        if left < right and overlapped and merged_erase_size <= 10:
            contents[i] = ("E", left, merged_erase_size)
            return True

        left = contents[i][1]
        right = contents[j][1] + contents[j][2]
        overlapped = contents[j][1] - 1 <= contents[i][1] + contents[i][2]
        merged_erase_size = right - left

        if left < right and overlapped and merged_erase_size <= 10:
            contents[i] = ("E", left, merged_erase_size)
            return True

        return False

    def optimize(self, command_buffer: list):
        optimized_buffer = command_buffer[:]
        for i in range(len(command_buffer)):
            optimized_buffer = self._optimize_adjacent(
                optimized_buffer, self.__compare_optimize_function
            )
        return optimized_buffer
