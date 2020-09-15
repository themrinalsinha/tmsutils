from itertools import chain
from typing    import (ItemsView, Iterator, KeysView, List,
                       Optional, Union, ValuesView)

# Error Handlers
def key_error(failing_key, original_path, raised_error):
    return KeyError(
        f"Cannot access key '{failing_key}' in path '{original_path}',"
        f" because of error: {repr(raised_error)}..."
    )

def index_error(failing_key, original_path, raised_error):
    return IndexError(
        f"Cannot access index '{failing_key}' in path '{original_path}',"
        f" because of error: {repr(raised_error)}..."
    )

def type_error(failing_key, original_path, item):
    return TypeError(
        f"Connot access key '{failing_key}' in path '{original_path}': "
        f"the element must be a dictionary or a list but is of type '{type(item)}'..."
    )


# Helper Functions
def _split(path: str, seperator: str) -> List[Union[str, int]]:
    result   = []
    sections = path.split(seperator)

    for section in sections:
        key, *indexes = section.split("[")
        result.append(key)
        if not indexes:
            continue

        try:
            for index in indexes:
                index = index[:-1]
                result.append(int(index))
        except ValueError:
            if index != "" and "]" not in index:
                raise ValueError(
                    f"Unable to access item '{index}' in key '{section}': "
                    "You can only provide integer to access list items."
                )
            else:
                raise ValueError(f"Key '{section}' is badly formated.")

    return result

def traverse(data: dict, keys: List[Union[str, int]], original_path: str):
    value = data
    try:
        for key in keys:
            value = value[key]
    except KeyError as error:
        raise key_error(key, original_path, error)
    except IndexError as error:
        raise index_error(key, original_path, error)
    except TypeError:
        raise type_error(key, original_path, value)
    return value


class DictManager:
    """
    DictManager is a simple wrapper over the built-in dict class

    It enables the standard dictionary API to operate on nested
    dictionaries and can operate across list items using given
    seperated string keys.

    Example:
        data    = {...}
        dictlab = DictManager(data)
        dictlab['dbg.saiyan'] = 'goku'
    """

    __slots__ = ("data", "seperator")

    def __init__(self, data: Optional[dict], seperator: str = ".") -> None:
        self.data      = data or {}
        self.seperator = seperator

    def __bool__(self) -> bool:
        return bool(self.data)

    def __contains__(self, path: str) -> bool:
        *keys, last_key = _split(path, self.seperator)
        try:
            item = traverse(data=self.data, keys=keys, original_path=path)
        except (KeyError, IndexError):
            return False

        try:
            item[last_key]
            return True
        except (KeyError, IndexError):
            return False

    def __delitem__(self, path: str) -> None:
        *keys, last_key = _split(path, self.seperator)
        item = traverse(data=self.data, keys=keys, original_path=path)

        try:
            del item[last_key]
        except KeyError as error:
            raise key_error(last_key, path, error)
        except IndexError as error:
            raise index_error(last_key, path, error)
        except TypeError:
            raise type_error(last_key, path, item)

    def __eq__(self, other) -> bool:
        return self.data == other

    def __getitem__(self, path: str):
        *keys, last_key = _split(path, self.seperator)
        item = traverse(data=self.data, keys=keys, original_path=path)

        try:
            return item[last_key]
        except KeyError as error:
            raise key_error(last_key, path, error)
        except IndexError as error:
            raise index_error(last_key, path, error)
        except TypeError:
            raise type_error(last_key, path, item)

    def __iter__(self) -> Iterator:
        return iter(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __ne__(self, other: object) -> bool:
        return not self.data == other

    def __setitem__(self, path: str, value) -> None:
        *keys, last_key = _split(path, self.seperator)
        item = traverse(data=self.data, keys=keys, original_path=path)

        try:
            item[last_key] = value
        except IndexError as error:
            raise index_error(last_key, path, error)
        except TypeError:
            raise type_error(last_key, path, item)

    def __str__(self) -> str:
        return str(self.data)

    def all(self, path: str):
        items = self[path]
        cls   = self.__class__
        return (cls(_dict, self.seperator) for _dict in items)

    def clear(self) -> None:
        return self.data.clear()

    def copy(self) -> dict:
        return self.data.copy()

    @classmethod
    def fromkeys(cls, sequence, value=None):
        return cls(dict.fromkeys(sequence, value))

    def get(self, path: str, default=None):
        try:
            return self[path]
        except (KeyError, IndexError) as error: # noqa
            return default

    def keys(self) -> KeysView:
        return self.data.items()

    def values(self) -> ValuesView:
        return self.data.values()

    def items(self) -> ItemsView:
        return self.data.items()

    def pop(self, path: str, *args):
        *keys, last_key = _split(path, self.seperator)

        try:
            item = traverse(data=self.data, keys=keys, original_path=path)
        except (KeyError, IndexError) as error:
            if args:
                return args[0]
            raise error

        try:
            return item.pop(last_key)
        except KeyError as error:
            if args:
                return args[0]
            raise key_error(last_key, path, error)
        except IndexError as error:
            if args:
                return args[0]
            raise index_error(last_key, path, error)
        except AttributeError as error: # noqa
            raise AttributeError(
                f"Unable to pop item '{last_key}' in key '{path}': "
                f"the element must be a dictionary or a list but is of type '{type(item)}'."
            )

    def popitem(self):
        return self.data.popitem()

    def setdefault(self, path: str, default=None):
        *keys, last_key = _split(path, self.seperator)
        item = traverse(data=self.data, keys=keys, original_path=path)

        try:
            return item[last_key]
        except KeyError:
            item[last_key] = default
            return default
        except IndexError as error:
            raise index_error(last_key, path, error)
        except TypeError:
            raise type_error(last_key, path, item)

    def update(self, data=None, **kwargs):
        data = data or {}
        try:
            data.update(kwargs)
            pairs = data.items()
        except AttributeError:
            pairs = chain(data, kwargs.items())

        for key, value in pairs:
            self.__setitem__(key, value)
