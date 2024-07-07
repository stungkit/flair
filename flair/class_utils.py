import importlib
import inspect
from typing import Any, Iterable, List, Optional, Type, TypeVar

T = TypeVar("T")


def get_non_abstract_subclasses(cls: Type[T]) -> Iterable[Type[T]]:
    for subclass in cls.__subclasses__():
        yield from get_non_abstract_subclasses(subclass)
        if inspect.isabstract(subclass):
            continue
        yield subclass


def get_state_subclass_by_name(cls: Type[T], cls_name: Optional[str]) -> Type[T]:
    for sub_cls in get_non_abstract_subclasses(cls):
        if sub_cls.__name__ == cls_name:
            return sub_cls
    raise ValueError(f"Could not find any class with name '{cls_name}'")


def lazy_import(group: str, module: str, *symbols: List[str]) -> List[Any]:
    try:
        imported_module = importlib.import_module(module)
    except ImportError:
        raise ImportError(
            f"Could not import {module}. Please install the optional '{group}' dependency. Via 'pip install flair[{group}]'"
        )
    if not symbols:
        return imported_module

    return [getattr(imported_module, symbol) for symbol in symbols]
