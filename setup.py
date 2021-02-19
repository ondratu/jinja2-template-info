"""package installation."""
import re
import importlib

from setuptools import setup  # type: ignore

REQUIREMENTS = ["Jinja2"]
if not hasattr(importlib, "resources"):
    REQUIREMENTS.append("importlib_resources")

METADATA = {}
with open("jinja2_template_info/__init__.py", "r") as info:
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
    packages=["jinja2_template_info"],
    package_data={"": ["py.typed", "template_info.html"]},
    data_files=[("share/doc/jinja2_template_info",
                 ["README.rst", "COPYING", "ChangeLog", "AUTHORS"]),
                ("share/doc/jinja2_template_info/examples",
                 ["test.html"])],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries"],
    install_requires=REQUIREMENTS,
    )
