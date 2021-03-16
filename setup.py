import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qsense",
    version="0.2.0",
    author="Matteo Redaelli",
    author_email="matteo.redaelli@gmail.com",
    description="qsense is a useful library and command line tool for qliksense",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/matteoredaelli/qsense",
    packages=setuptools.find_packages(),
    license="GPL",
    entry_points = {
        'console_scripts': ['qsense=qsense.command_line:main'],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'requests_ntlm', 'qsapi', 'fire'],
    python_requires='>=3.6',
)
