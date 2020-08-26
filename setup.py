"""package installation."""
import re

from setuptools import setup

METADATA = {}
with open("jinja2_template_info.py", "r") as info:
    METADATA = dict(re.findall(r'__([a-z_]+)__ = "([^"]+)"', info.read()))


def doc():
    """Return README.rst content."""
    with open("README.rst", "r", encoding="utf-8") as readme:
        return readme.read().strip()


setup(
    name="Jinja2-template_info",
    version=METADATA["version"],
    author=METADATA["author_name"],
    author_email=METADATA["author_email"],
    description=METADATA["description"],
    long_description=doc(),
    long_description_content_type="text/x-rst",
    url=METADATA["url"],
    license=METADATA["license"],
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
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries"],
    install_requires=["Jinja2"],
    )
