"""Setup for rhasspyrasa_nlu_hermes"""
import os

import setuptools

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, "README.md"), "r") as readme_file:
    long_description = readme_file.read()

with open(os.path.join(this_dir, "requirements.txt"), "r") as requirements_file:
    requirements = requirements_file.read().splitlines()

with open(os.path.join(this_dir, "VERSION"), "r") as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name="rhasspy-rasa-nlu-hermes",
    version=version,
    author="Michael Hansen",
    author_email="hansen.mike@gmail.com",
    url="https://github.com/rhasspy/rhasspy-rasa-nlu-hermes",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)
