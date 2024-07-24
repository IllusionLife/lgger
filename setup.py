# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="lgger",
    version="0.1.3.1",
    description="A package for writing logs to log files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IllusionLife/lgger",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Logging",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="logging, simple, files",
    packages=["lgger", "lgger.lgger_src", "lgger.templates"],
    python_requires=">=3.7, <4",
    package_data={
        "configurations": ["lgger/config/lgger.conf"],
    },
    zip_safe=False,
)
