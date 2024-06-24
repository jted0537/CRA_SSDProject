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

    def _optimize_adjacent(
        self, command_buffer: list, compare_optimize_function: callable
    ):
        should_delete = [False] * len(command_buffer)

        for i in range(len(command_buffer) - 1, 0, -1):

            if compare_optimize_function(command_buffer, i, i - 1):
                should_delete[i - 1] = True
                should_delete[i] = False
                # The optimized element should not be deleted, even if it is used by prior optimization phase

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


class ReduceEraseDuplication(Optimizer):
    def __compare_function(self, content_i, content_j):
        if (
            content_i[0] == "E"
            and content_j[0] == "E"
            and content_i[1] <= content_j[1]
            and content_j[1] + content_j[2] <= content_i[1] + content_i[2]
        ):
            return True

        return False

    def optimize(self, command_buffer: list):
        return self._traverse_and_optimize(command_buffer, self.__compare_function)


class MergeAdjacentErase(Optimizer):
    def __compare_optimize_function(self, contents: list, i: int, j: int):

        left = contents[j][1]
        right = contents[i][1] + contents[i][2]
        overlapped = contents[i][1] - 1 <= contents[j][1] + contents[j][2]
        merged_erase_size = right - left

        if (
            contents[i][0] == "E"
            and contents[j][0] == "E"
            and left <= right
            and overlapped
            and merged_erase_size <= 10
        ):
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
