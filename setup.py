# Always prefer setuptools over distutils
from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
setup(
    name="lgger",
    version="0.1.5",
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
    python_requires=">=3.7, <4",

    package_data={"":["templates/*.template"]},
    include_package_data=True,
)
