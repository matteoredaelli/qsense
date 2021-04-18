# Copyright (c) 2021 Matteo Redaelli
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qsense",
    version="0.6.2",
    author="Matteo Redaelli",
    author_email="matteo.redaelli@gmail.com",
    description="qsense is a python library and a command line tool for qliksense",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matteoredaelli/qsense",
    packages=setuptools.find_packages(),
    license="GPL",
    entry_points={
        "console_scripts": ["qsense=qsense.command_line:main"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "requests_ntlm", "qsapi", "pyqlikengine", "fire"],
    python_requires=">=3.6",
)
