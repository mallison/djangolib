# TODO is this bad manners?
from setuptools import setup, find_packages

setup(
    name="djangolib",
    version="0.1a1",
    description="Library of miscellaneous handy django stuff",
    author="Mark Allison",
    author_email="mallison77@gmail.com",
    package_dir={'djangolib': 'djangolib'},
    packages=find_packages(),
    include_package_data=True,
    setup_requires=['setuptools-git'],  # to find package data
    install_requires=['distribute']
)
