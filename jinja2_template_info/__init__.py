# -*- coding: utf-8 -*-
"""Jinja2 Extension for template debugging."""

try:
    from importlib.resources import files  # type: ignore
except ImportError:
    from importlib_resources import files

from jinja2 import Environment, FileSystemLoader, DebugUndefined, \
    contextfunction
from jinja2.ext import Extension

__version__ = "0.2.2"
__date__ = "19 Feb 2021"
__author_name__ = "Ondřej Tůma"
__author_email__ = "mcbig@zeropage.cz"
__author__ = f"{__author_name__} <{__author_email__}>"
__license__ = "BSD"
__description__ = "Jinja2 Extension for template debugging."
__url__ = "https://github.com/ondratu/jinja2-template-info"


@contextfunction
def ctx(context):
    """Return Jinja2 context.

    See http://jinja.pocoo.org/docs/2.10/api/#the-context
    """
    return context


class TemplateInfo():
    """Object to store template information.

    * context - function returns Jinja Context object.
    * data - key value arguments for template render method (dict).
    * undefined - list of variables, which was not found in template.
    * template - filename of template.

    """
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.context = ctx
        self.data = None
        self.undefined = []
        self.template = None


class TemplateInfoExtension(Extension):
    """Jinja2 Extension which append template_info object to environment.

    >>> try:
    ...     from importlib.resources import files
    ... except ImportError:
    ...     from importlib_resources import files
    >>> from jinja2 import Environment, FileSystemLoader
    >>> from jinja2_template_info import TemplateInfoExtension
    >>> data = {"title":"Title"}
    >>> path = (files('jinja2_template_info'), "./")
    >>> env = Environment(loader=FileSystemLoader(path),
    ...                   extensions=[TemplateInfoExtension])
    >>> env.globals["template_info"].data = data.copy()
    >>> env.globals["template_info"].template = "test.html"
    >>> template = env.get_template("test.html")
    >>> template.render(data)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '<!DOCTYPE html>...</html>'
    """
    def __init__(self, environment):
        super().__init__(environment)
        info = TemplateInfo()

        class MissingUndefined(DebugUndefined):
            """Debug class for _miss_ variable in jinja."""
            def __recursion__(self, *args, **kwargs):
                # pylint: disable=unused-argument
                info.undefined.append(self._undefined_name)
                return MissingUndefined()

            __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
                __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
                __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
                __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = __int__ = \
                __float__ = __complex__ = __pow__ = __rpow__ = \
                __recursion__

            def __getattribute__(self, name):
                if name[0] == '_':
                    return DebugUndefined.__getattribute__(self, name)
                info.undefined.append(self._undefined_name)
                return MissingUndefined(name=name)

            def __str__(self):
                if self._undefined_name is None:
                    return ''
                info.undefined.append(self._undefined_name)
                return '[Undefined] %s' % self._undefined_name

        environment.undefined = MissingUndefined
        environment.globals['template_info'] = info

    def parse(self, parser):
        """Only compatibility definition."""


def render(filename, path, **kwargs):
    """Render template with some info variables.

    >>> from jinja2_template_info import render
    >>> render("test.html", "./", debug=True,
    ...        code_variable="Variable from code")
    ...        # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '<!DOCTYPE html>...</html>'
    """
    info_path = files('jinja2_template_info')
    if isinstance(path, (list, tuple)):
        path = tuple(path)+(info_path,)
    else:  # str
        path = (info_path, path)

    env = Environment(loader=FileSystemLoader(path))
    if kwargs.get("debug"):
        env.add_extension(TemplateInfoExtension)
        env.globals['template_info'].data = kwargs.copy()
        env.globals['template_info'].template = filename

    template = env.get_template(filename)
    return template.render(kwargs)
