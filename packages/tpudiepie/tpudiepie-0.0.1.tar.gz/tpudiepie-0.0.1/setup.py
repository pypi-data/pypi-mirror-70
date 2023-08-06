#!/usr/bin/env python3

import setuptools
import os

package_name = "tpudiepie"
binary_name = "die"
packages = setuptools.find_packages(
    include=[package_name, "{}.*".format(package_name)]
)

# Version info -- read without importing
_locals = {}
with open(os.path.join(package_name, "_version.py")) as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

# Frankenstein long_description: changelog note + README
long_description = """
To find out what's new in this version of tpudiepie, please see `the repo
<https://github.com/shawwn/tpudiepie>`_.

{}
""".format(
    open("README.rst").read()
)

setuptools.setup(
    name=package_name,
    version=version,
    description="TPU management",
    license="BSD",
    long_description=long_description,
    author="Shawn Presser",
    author_email="shawnpresser@gmail.com",
    url="https://github.com/shawwn/tpudiepie",
    install_requires=[
        'Click>=7.1.2',
        'six>=1.11.0',
        'ring>=0.7.3',
        'moment>=0.0.10',
    ],
    packages=packages,
    entry_points={
        "console_scripts": [
            "{} = {}.program:cli".format(package_name, package_name),
            "{} = {}.program:cli".format(binary_name, package_name),
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Software Distribution",
        "Topic :: System :: Systems Administration",
    ],
)

