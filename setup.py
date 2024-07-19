# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="lgger",
    version="0.1.0",
    description="A package for writing logs to log files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",  # Optional
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Logging",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="logging, simple, files",
    package_dir={"": "logger_src"},
    packages=find_packages(where="logger_src"),
    python_requires=">=3.7, <4",
    # # If there are data files included in your packages that need to be
    # # installed, specify them here.
    # package_data={  # Optional
    #     "sample": ["package_data.dat"],
    # },
)