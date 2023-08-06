import importlib
import inspect
from typing import Any, Tuple


def get_object(name: str) -> Any:
    """Reutrns an object specified by `name`.

    Args:
        name: Object name.

    Examples:
        >>> import inspect
        >>> obj = get_object('mkapi.core')
        >>> inspect.ismodule(obj)
        True
        >>> obj = get_object('mkapi.core.base')
        >>> inspect.ismodule(obj)
        True
        >>> obj = get_object('mkapi.core.node.Node')
        >>> inspect.isclass(obj)
        True
        >>> obj = get_object('mkapi.core.node.Node.get_markdown')
        >>> inspect.isfunction(obj)
        True
    """
    names = name.split(".")
    for k in range(len(names), 0, -1):
        module_name = ".".join(names[:k])
        try:
            obj = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        for attr in names[k:]:
            obj = getattr(obj, attr)
        return obj
    raise ValueError(f"Could not find object: {name}")


def split_prefix_and_name(obj) -> Tuple[str, str]:
    """Split an object full name into prefix and name.

    Examples:
        >>> import inspect
        >>> obj = get_object('mkapi.core')
        >>> split_prefix_and_name(obj)
        ('mkapi', 'core')
        >>> obj = get_object('mkapi.core.base')
        >>> split_prefix_and_name(obj)
        ('mkapi.core', 'base')
        >>> obj = get_object('mkapi.core.node.Node')
        >>> split_prefix_and_name(obj)
        ('mkapi.core.node', 'Node')
        >>> obj = get_object('mkapi.core.node.Node.get_markdown')
        >>> split_prefix_and_name(obj)
        ('mkapi.core.node.Node', 'get_markdown')
    """
    if isinstance(obj, property):
        obj = obj.fget
    if inspect.ismodule(obj):
        prefix, _, name = obj.__name__.rpartition(".")
    else:
        module = obj.__module__
        qualname = obj.__qualname__
        if "." not in qualname:
            prefix, name = module, qualname
        else:
            prefix, _, name = qualname.rpartition(".")
            prefix = ".".join([module, prefix])
        if prefix == "__main__":
            prefix = ""
    return prefix, name


def get_sourcefile_and_lineno(obj) -> Tuple[str, int]:
    if isinstance(obj, property):
        obj = obj.fget
    try:
        sourcefile = inspect.getsourcefile(obj) or ""
    except TypeError:
        sourcefile = ""
    try:
        lineno = inspect.getsourcelines(obj)[1]
    except (TypeError, OSError):
        lineno = -1
    return sourcefile, lineno
