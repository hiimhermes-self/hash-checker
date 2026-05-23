import tempfile
import os
from pathlib import Path
from hash_checker.__main__ import hash_file, hash_directory, verify_checksum_file, main


def test_hash_file_md5():
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("hello")
        path = f.name
    try:
        assert hash_file(path, "md5") == "5d41402abc4b2a76b9719d911017c592"
    finally:
        os.remove(path)


def test_hash_directory():
    with tempfile.TemporaryDirectory() as d:
        Path(d, "a.txt").write_text("alpha")
        Path(d, "sub").mkdir()
        Path(d, "sub", "b.txt").write_text("beta")
        result = hash_directory(d, "sha256")
        assert "a.txt" in result
        assert "sub/b.txt" in result
        assert len(result) == 2


def test_verify_checksum_file():
    with tempfile.TemporaryDirectory() as d:
        Path(d, "f.txt").write_text("hello")
        manifest = os.path.join(d, "sums.txt")
        with open(manifest, "w") as f:
            f.write("5d41402abc4b2a76b9719d911017c592  f.txt\n")
        ok, failures = verify_checksum_file(manifest, d, "md5")
        assert len(ok) == 1
        assert len(failures) == 0


def test_main_help(capsys):
    try:
        main(["--help"])
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert "hash-checker" in captured.out


def test_main_version(capsys):
    try:
        main(["--version"])
    except SystemExit as e:
        assert e.code == 0
    captured = capsys.readouterr()
    assert "0.1.1" in captured.out
