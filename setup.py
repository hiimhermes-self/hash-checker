from setuptools import setup, find_packages

setup(
    name="hash-checker",
    version="0.1.1",
    description="Bulk file hash verification tool. SHA256/MD5/SHA1/SHA512/BLAKE2b.",
    author="hiimhermes-self",
    url="https://github.com/hiimhermes-self/hash-checker",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "hash-checker=hash_checker.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
