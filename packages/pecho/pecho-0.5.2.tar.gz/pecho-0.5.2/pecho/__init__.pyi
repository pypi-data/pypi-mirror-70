import sys
from typing import Any, Callable, Dict, List, Optional, Protocol, TextIO, TypeVar, Union, overload

__all__: List[str]

try:
    import importlib.metadata
except ImportError:
    __version__: None
else:
    __version__: str

_PrintFuncArg = TypeVar('_PrintFuncArg')
_PrintFuncReturn = TypeVar('_PrintFuncReturn')

class PrintFuncText(Protocol):
    def __call__(self, __text: _PrintFuncArg, *__args: Any, **__kwargs: Any) -> _PrintFuncReturn: ...

class PrintFuncObjects(Protocol):
    def __call__(self, *__objects: _PrintFuncArg, **__kwargs: Any) -> _PrintFuncReturn: ...

@overload
def echo(
    __text: _PrintFuncArg,
    newline: bool = ...,
    newline_char: str = ...,
    end: str = ...,
    print_func: PrintFuncText = ...,
    print_func_kwargs: Dict[str, Any] = ...,
) -> _PrintFuncReturn: ...
@overload
def echo(
    *objects: _PrintFuncArg,
    newline: bool = ...,
    newline_char: str = ...,
    end: str = ...,
    print_func_kwargs: Dict[str, Any] = ...,
) -> _PrintFuncReturn: ...
def echo(
    *objects: _PrintFuncArg,
    newline: bool = ...,
    newline_char: str = ...,
    end: str = ...,
    print_func: PrintFuncObjects = ...,
    print_func_kwargs: Dict[str, Any] = ...,
) -> _PrintFuncReturn: ...
