from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

__author__ = "Denis Mulyalin <d.mulyalin@gmail.com>"

setup(
    name="N2G",
    version="0.1.2",
    author="Denis Mulyalin",
    author_email="d.mulyalin@gmail.com",
    description="Need To Graph",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dmulyalin/N2G",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['n2g=N2G.utils.N2G_cli:cli_tool']
    },
    package_data = {
        'N2G': ['utils/ttp_templates/*/*.txt']
    }
)