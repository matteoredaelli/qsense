import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pysense",
    version="0.1.0",
    author="Matteo Redaelli",
    author_email="matteo.redaelli@gmail.com",
    description="pysense is a useful library / command line tool for qliksense",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/matteo.redaelli/pysense",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['pysense=pysense.command_line:main'],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE V3 OR LATER (GPLV3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'requests_ntlm', 'qsapi', 'fire'],
    python_requires='>=3.6',
)
