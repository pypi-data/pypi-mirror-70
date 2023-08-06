from functools import lru_cache
from importlib import import_module
import os
import sys
import typing as t


def import_all_names(_file, _name):
    """
    Util for a tricky dynamic import of all names from all submodules.
    Use it in the __init__.py using following idiom:

        import_all_names(__file__, __name__)

    Supports __all__ attribute of the submodules.
    """
    path = os.path.dirname(os.path.abspath(_file))
    parent_module = sys.modules[_name]

    dir_list = []
    for py in [filename[:-3] for filename in os.listdir(path)
               if filename.endswith('.py') and filename != '__init__.py']:
        module = __import__('.'.join([_name, py]), fromlist=[py])
        module_names = getattr(module, '__all__', None) or dir(module)
        objects = dict(
            (name, getattr(module, name))
            for name in module_names
            if not name.startswith('_')
        )
        for name, obj in objects.items():
            if hasattr(parent_module, name) and \
               getattr(parent_module, name) is not obj:
                msg = (
                    "Function import_all_names hit upon conflicting "
                    "names. '{0}' is already imported to {1} module."
                ).format(name, module)
                import warnings
                warnings.warn(msg)
            setattr(parent_module, name, obj)
        dir_list.extend(objects)
    parent_module.__dir__ = lambda: dir_list


# noinspection PyUnboundLocalVariable
def import_dotted_path(dotted_path: str) -> t.Type:
    """
    Import a dotted module path and return the attribute/class designated by
    the last name in the path. Raise ImportError if the import failed.

    Code taken from: django.utils.module_loading,import_string v 1.9
    """
    try:
        module_path, qual_name = dotted_path.rsplit(':', 1) \
            if ':' in dotted_path else dotted_path.rsplit('.', 1)
    except ValueError as e:
        msg = "'%s' doesn't look like a module path" % dotted_path
        raise ImportError(msg) from e

    obj = import_module(module_path)

    try:
        for chunk in qual_name.split('.'):
            obj = getattr(obj, chunk)
    except AttributeError as e:
        msg = "Module '%s' does not define a '%s' attribute/class" % (
            module_path, qual_name)
        raise ImportError(msg) from e
    return obj


@lru_cache(maxsize=None)
def get_dotted_path(target: t.Union[t.Type, t.Callable]) -> str:
    """
    Constructs python qualified name for the `target`. The function caches every result.
    """
    qualname = getattr(target, '__qualname__', None)
    module_name = getattr(target, '__module__', None)
    return f"{module_name}.{qualname}" if module_name and qualname \
        else qualname if not module_name else ''


def maybe_dotted(target: t.Union[str, t.Type]) -> t.Type:
    """
    Imports a Python qualified name given in the target.
    """
    if isinstance(target, str):
        return import_dotted_path(target)
    return target
