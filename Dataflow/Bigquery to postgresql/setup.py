from setuptools import setup, find_packages

requires = [
"apache-beam[gcp]==2.35.0",
"beam-nuggets==0.18.1"
]

setup(
name="test",
version="1.0.0",
author='Vignesh Sekar',
author_email='vsekar@deloitte.com',
description="Apache Beam-Python pipeline for getting data test data",
packages=find_packages(),
install_requires=requires,
)