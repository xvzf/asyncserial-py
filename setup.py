from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="asyncserial",
    version="0.1.0",
    description="Asyncio wrapper for pyserial",
    long_description=long_description,
    url="https://github.com/xvzf/asyncserial-py",
    author="Matthias Riegler",
    author_email="matthias@xvzf.tech",
    python_requires='>=3.5',

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Framework :: AsyncIO",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="serial pyserial async asyncio",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["pyserial"],
    tests_require=['pytest', 'uvloop'],

    extras_require={  # Optional
        "uvloop support": ["uvloop"],
    },

    project_urls={  # Optional
        "Bug Reports": "https://github.com/xvzf/asyncserial-py/issues",
        "Source": "https://github.com/xvzf/asyncserial-py/",
    },

)
