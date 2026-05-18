from setuptools import setup, find_packages

setup(
    name="hash-checker",
    version="0.1.0",
    description="Dosyalarin hash'lerini toplu dogrulayan arac. SHA256/MD5/SHA1.",
    packages=find_packages(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "hash-checker=hash_checker:main",
        ],
    },
)
