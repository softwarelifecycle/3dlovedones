from pathlib import Path
import shutil

def tryparse(string, base=10):
    """
        Usage:>>> if (n := tryparse("123")) is not None:
    ...     print(n)
    ...
    123
     if (n := tryparse("abc")) is None:
    ...     print(n)
    None
    """

    try:
        return int(string, base=base)
    except ValueError:
        return None

def movefiles(src_path, trg_path):
    for src_file in Path(src_path).glob('*.*'):
        shutil.copy(src_file, trg_path)