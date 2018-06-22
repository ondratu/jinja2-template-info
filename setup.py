"""package installation."""
from setuptools import setup
from io import open

from jinja2_template_info import __version__, __author__, \
    __email__, __license__, __doc__ as description


def doc():
    """Return README.rst content."""
    with open("README.rst", "r", encoding="utf-8") as readme:
        return readme.read().strip()


setup(
    name="Jinja2-template_info",
    version=__version__,
    author=__author__,
    author_email=__email__,
    description=description,
    long_description=doc(),
    long_description_content_type="text/x-rst",
    url="https://github.com/ondratu/jinja2-template-info",
    license=__license__,
    py_modules=["jinja2_template_info"],
    data_files=[("share/doc/jinja2_template_info",
                 ["README.rst", "COPYING", "ChangeLog", "AUTHORS"]),
                ("share/doc/jinja2_template_info/examples",
                 ["test.html"]),
                ("share/jinja2_template_info/templates",
                 ["template_info.html"])],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries"],
    )
