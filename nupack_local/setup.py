from setuptools import setup, find_packages

setup(
    name='nupack',
    version='4.0.0.23',
    packages=find_packages(),
    install_requires=[
        'scipy>=1.0',
        'numpy>=1.17',
        'pandas>=1.1.0',
        'jinja2>=2.0'
    ],
    # additional metadata and configurations can go here
)