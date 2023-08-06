from typing import Callable, Dict, Any, Iterator, MutableMapping, Type

import numpy as np


class ObjectFormatter(Dict[str, Callable[[np.ndarray], np.ndarray]],
                      MutableMapping[str, Callable[[np.ndarray], np.ndarray]]):
    """
    A dictionary to contain mappings for formatting objects. Some numpy objects
    should be cast to other types, e.g. the :class:`decimal.Decimal` type cannot
    operate with :class:`np.float`. These mappings are defined in this class.

    Each mapping must define a function that takes a :class:`np.ndarray` and
    returns a :class:`np.ndarray`.

    The key for each mapping is the name of the type of the actual value,
    looked up from the first element of the :class:`np.ndarray`, i.e.
    ``type(array[0]).__name__``.
    """
    test_array = np.arange(4)

    def __setitem__(self, dtype: str, value: Callable[[np.ndarray], np.ndarray]) -> None:
        """
        Set the dtype formatter.
        """
        try:
            if not isinstance(value(self.test_array), np.ndarray):
                raise ValueError(
                    'Must provide a function that takes an ``np.ndarray`` and returns '
                    'an np.ndarray.')
        except Exception as e:
            raise ValueError(
                'Must provide a function that takes an ``np.ndarray`` and returns '
                'an np.ndarray.')

        dict.__setitem__(self, dtype, value)

    def __getitem__(self, dtype: str) -> Callable[[np.ndarray], np.ndarray]:
        """
        Get the dtype formatter.
        """
        return dict.__getitem__(self, dtype)

    def __delitem__(self, dtype: str) -> None:
        """
        Delete the dtype formatter.
        """
        dict.__delitem__(self, dtype)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if self.__len__() < 1:
            return r'{}'
        return '{' + '\n'.join(f'{c}: {v}' for c, v in self.items()) + '}'

    def __iter__(self) -> Iterator[Any]:
        yield from dict.__iter__(self)

    def __len__(self) -> int:
        return dict.__len__(self)

    def copy(self) -> Dict[str, Any]:
        return {k: dict.__getitem__(self, k) for k in self}
