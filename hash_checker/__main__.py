#!/usr/bin/env python3
"""Dosyalarin hash'lerini toplu dogrulayan arac. SHA256/MD5/SHA1."""
import hashlib
import sys
import os
from pathlib import Path

SUPPORTED = {"sha256": hashlib.sha256, "md5": hashlib.md5, "sha1": hashlib.sha1}

def hash_file(filepath, algo="sha256"):
    h = SUPPORTED[algo]()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def hash_directory(directory, algo="sha256"):
    results = {}
    for root, _, files in os.walk(directory):
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            try:
                results[fpath] = hash_file(fpath, algo)
            except Exception as e:
                results[fpath] = f"ERROR: {e}"
    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: hash-checker <file_or_dir> [algo:sha256|md5|sha1]")
        sys.exit(1)
    target = sys.argv[1]
    algo = sys.argv[2] if len(sys.argv) > 2 else "sha256"
    
    if algo not in SUPPORTED:
        print(f"Desteklenen algoritmalar: {list(SUPPORTED.keys())}")
        sys.exit(1)
    
    if os.path.isdir(target):
        print(f"[{algo.upper()}] {target} dizini taraniyor...")
        results = hash_directory(target, algo)
        for path, digest in results.items():
            print(f"  {digest}  {path}")
    elif os.path.isfile(target):
        digest = hash_file(target, algo)
        print(f"{digest}  {target}")
    else:
        print(f"Hedef bulunamadi: {target}")
        sys.exit(1)

if __name__ == "__main__":
    main()
