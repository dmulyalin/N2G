from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

__author__ = "Denis Mulyalin <d.mulyalin@gmail.com>"

setup(
    name="N2G",
    version="0.0.1",
    author="Denis Mulyalin",
    author_email="d.mulyalin@gmail.com",
    description="Need To Graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmulyalin/n2g",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)