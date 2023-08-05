"""Setup script for rhasspy-fuzzywuzzy package"""
import os

import setuptools

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), "r") as readme_file:
    long_description = readme_file.read()

with open("requirements.txt", "r") as requirements_file:
    requirements = requirements_file.read().splitlines()

with open("VERSION", "r") as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="rhasspy-fuzzywuzzy",
    version=version,
    author="Michael Hansen",
    author_email="hansen.mike@gmail.com",
    url="https://github.com/rhasspy/rhasspy-fuzzywuzzy",
    packages=setuptools.find_packages(),
    package_data={"rhasspyfuzzywuzzy": ["py.typed"]},
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
