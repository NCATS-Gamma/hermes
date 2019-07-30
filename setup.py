"""Setup file for hermes package."""
from setuptools import setup

setup(
    name='hermes',
    version='0.1.0-dev',
    author='Patrick Wang',
    author_email='patrick@covar.com',
    url='https://github.com/NCATS-Gamma/hermes',
    description='Pipelining for NCATS Translator services',
    packages=['hermes'],
    include_package_data=True,
    zip_safe=False,
    license='MIT',
    python_requires='>=3.7',
)
