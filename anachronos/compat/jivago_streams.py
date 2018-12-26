# Copyright Jivago framework
# Kento A. Lauzon 2018
# Licensed under MIT License
# https://github.com/keotl/jivago

import itertools
from typing import Iterable, Callable, Iterator, Optional, Tuple, Any


class Stream(object):

    def __init__(self, *iterables: Iterable):
        self.iterable = itertools.chain(*iterables)

    def map(self, fun: Callable) -> "Stream":
        if self.__should_expand(fun):
            return Stream(map(lambda tup: fun(*tup), self.iterable))
        else:
            return Stream(map(fun, self.iterable))

    def filter(self, fun: Callable) -> "Stream":
        if self.__should_expand(fun):
            return Stream(filter(lambda tup: fun(*tup), self.iterable))
        else:
            return Stream(filter(fun, self.iterable))

    def forEach(self, fun: Callable) -> None:
        if self.__should_expand(fun):
            for i in self:
                fun(*i)
        else:
            for i in self:
                fun(i)

    def anyMatch(self, fun: Callable) -> bool:
        return any(self.map(fun))

    def allMatch(self, fun: Callable) -> bool:
        return all(self.map(fun))

    def firstMatch(self, fun: Callable) -> Optional:
        if self.__should_expand(fun):
            for i in self:
                if fun(*i):
                    return i
        else:
            for i in self:
                if fun(i):
                    return i
        return None

    def noneMatch(self, fun: Callable) -> bool:
        return not self.anyMatch(fun)

    def flat(self) -> "Stream":
        return Stream(itertools.chain(*self))

    def toList(self) -> list:
        return list(self)

    def toSet(self) -> set:
        return set(self)

    def toDict(self) -> dict:
        return dict(self)

    def toTuple(self) -> tuple:
        return tuple(self)

    def __should_expand(self, fun: Callable) -> bool:
        if self.__is_builtin_function(fun):
            return False
        if type(fun) == type and hasattr(fun.__init__, "__code__"):
            return fun.__init__.__code__.co_argcount > 2
        if hasattr(fun, "__code__"):
            return fun.__code__.co_argcount > 1
        return False

    def __is_builtin_function(self, fun: Callable) -> bool:
        return type(fun) == type(abs)

    def count(self) -> int:
        if hasattr(self.iterable, '__len__'):
            return len(self.iterable)
        return self.reduce(0, lambda accumulator, element: accumulator + 1)

    def reduce(self, start_value: object, reducer: Callable[[Any, object], Any]):
        """e.g. lambda accumulator, element: accumulator + element"""
        accumulator = start_value
        for element in self:
            accumulator = reducer(accumulator, element)
        return accumulator

    def __iter__(self) -> Iterator:
        return iter(self.iterable)

    @staticmethod
    def zip(*iterables: Iterable) -> "Stream":
        return Stream(zip(*iterables))

    def unzip(self) -> Tuple[tuple, ...]:
        return tuple(zip(*self))

    @staticmethod
    def of(*args) -> "Stream":
        return Stream(args)

    def sum(self):
        return sum(self)

    def min(self):
        return min(self)

    def max(self):
        return max(self)

    def take(self, number: int) -> "Stream":
        return Stream(itertools.islice(self, number))

    @staticmethod
    def range(*args) -> "Stream":
        if len(args) == 0:
            return Stream(itertools.count())
        else:
            return Stream(range(*args))
