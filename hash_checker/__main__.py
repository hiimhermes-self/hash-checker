#!/usr/bin/env python3
"""Dosyalarin hash'lerini toplu dogrulayan arac. SHA256/MD5/SHA1."""
import argparse
import hashlib
import os
import sys
from pathlib import Path

__version__ = "0.1.1"

SUPPORTED_ALGORITHMS = {"sha256", "md5", "sha1", "sha512", "blake2b"}


def hash_file(filepath: str, algorithm: str = "sha256", block_size: int = 8192) -> str:
    """Compute hash of a single file."""
    hasher = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_directory(directory: str, algorithm: str = "sha256") -> dict:
    """Recursively hash all files under directory."""
    results = {}
    base = Path(directory)
    for path in base.rglob("*"):
        if path.is_file():
            try:
                rel = str(path.relative_to(base))
                results[rel] = hash_file(str(path), algorithm)
            except (OSError, PermissionError):
                continue
    return results


def write_checksum_file(files_dict: dict, output_path: str, algorithm: str = "sha256") -> None:
    """Write GNU-style checksum file."""
    with open(output_path, "w", encoding="utf-8") as f:
        for name, digest in sorted(files_dict.items()):
            f.write(f"{digest}  {name}\n")


def verify_checksum_file(checksum_path: str, base_dir: str, algorithm: str = "sha256") -> tuple:
    """Verify files against a checksum manifest. Returns (ok, failures)."""
    ok, failures = [], []
    with open(checksum_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("  ", 1)
            if len(parts) != 2:
                parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            expected, name = parts
            filepath = os.path.join(base_dir, name)
            if not os.path.isfile(filepath):
                failures.append((name, "MISSING", expected, ""))
                continue
            actual = hash_file(filepath, algorithm)
            if actual == expected:
                ok.append(name)
            else:
                failures.append((name, "MISMATCH", expected, actual))
    return ok, failures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hash-checker",
        description="Bulk file hash verification tool. Supports SHA256, MD5, SHA1, SHA512, BLAKE2b.",
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-a", "--algorithm", default="sha256", choices=sorted(SUPPORTED_ALGORITHMS),
                        help="Hash algorithm (default: sha256)")
    parser.add_argument("-r", "--recursive", action="store_true",
                        help="Recursively scan directories")
    parser.add_argument("-o", "--output", default=None,
                        help="Write checksums to file")
    parser.add_argument("-c", "--check", default=None,
                        help="Verify against checksum file")
    parser.add_argument("paths", nargs="*", help="Files or directories to hash")
    return parser


def main(args=None):
    parser = build_parser()
    opts = parser.parse_args(args)

    if opts.check:
        if not opts.paths:
            base_dir = "."
        else:
            base_dir = opts.paths[0]
        ok, failures = verify_checksum_file(opts.check, base_dir, opts.algorithm)
        print(f"[hash-checker] {len(ok)} OK, {len(failures)} FAILED")
        for name, reason, expected, actual in failures:
            print(f"  FAIL {name}: {reason}")
            if actual:
                print(f"    expected: {expected}")
                print(f"    actual:   {actual}")
        sys.exit(0 if not failures else 1)

    if not opts.paths:
        parser.print_help()
        sys.exit(0)

    all_hashes = {}
    for p in opts.paths:
        path = Path(p)
        if path.is_file():
            all_hashes[str(path)] = hash_file(str(path), opts.algorithm)
        elif path.is_dir():
            if opts.recursive:
                for rel, digest in hash_directory(str(path), opts.algorithm).items():
                    all_hashes[f"{path}/{rel}"] = digest
            else:
                for child in sorted(path.iterdir()):
                    if child.is_file():
                        all_hashes[str(child)] = hash_file(str(child), opts.algorithm)
        else:
            print(f"Warning: skipping non-existent path: {p}", file=sys.stderr)

    for name, digest in sorted(all_hashes.items()):
        print(f"{digest}  {name}")

    if opts.output:
        write_checksum_file(all_hashes, opts.output, opts.algorithm)
        print(f"[hash-checker] Wrote {len(all_hashes)} entries to {opts.output}")


if __name__ == "__main__":
    main()
