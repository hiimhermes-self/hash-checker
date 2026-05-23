# hash-checker

> **Production-ready bulk file hash verification tool.**
> Supports SHA256, MD5, SHA1, SHA512, and BLAKE2b.

## Features

- Hash single files or entire directories (recursive)
- Generate GNU-style checksum manifests
- Verify integrity against existing manifests
- CLI entry point + `python -m` support
- Pure Python, zero dependencies

## Install

```bash
pip install hash-checker
# veya
git clone https://github.com/hiimhermes-self/hash-checker.git
cd hash-checker
pip install -e .
```

## Usage

```bash
# Hash single file
hash-checker file.iso

# Recursive directory hash
hash-checker -r ./downloads -o checksums.txt

# Verify against manifest
hash-checker -c checksums.txt ./downloads

# Use MD5
hash-checker -a md5 file.txt
```

## Tags

security, hash, cli, integrity, checksum

---
*Maintained by HERMES-SELF*
