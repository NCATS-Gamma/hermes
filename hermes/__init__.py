"""Make this a pkgutil-style namespace package.

Required for importlib.resources to work properly.
https://packaging.python.org/guides/packaging-namespace-packages/
"""
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
