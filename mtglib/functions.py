"""Useful functions that don't fit anywhere else."""

def is_string(obj):
    """Python 2 and 3 compatible string determinor."""
    try:
        return isinstance(obj, basestring)
    except NameError:
        return isinstance(obj, str)