from pathlib import Path
from unittest import mock

import pytest

from nibabies.utils.misc import _check_fname


def test_check_fname(tmp_path):
    """Test the _check_fname utility function."""
    fpath = Path(tmp_path) / "test_file.txt"
    fpath.touch()
    fpath_path = _check_fname(fpath, must_exist=True)
    assert isinstance(fpath_path, Path)

    # If file is not readable, we should raise an error
    orig_perms = fpath.stat().st_mode
    fpath.chmod(0)
    # We have to use mock here because pytest might be run as root
    with mock.patch("os.access", return_value=False):
        with pytest.raises(PermissionError):
            _check_fname(fpath)
    fpath.chmod(orig_perms)

    # We should raise an error if the file does not exist
    fpath.unlink()
    with pytest.raises(FileNotFoundError):
        _check_fname(fpath, must_exist=True)