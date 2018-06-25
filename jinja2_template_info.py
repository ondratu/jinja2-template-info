# -*- coding: utf-8 -*-
"""Jinja2 Extension for template debugging."""

from jinja2 import Environment, FileSystemLoader, DebugUndefined, \
    contextfunction
from jinja2.ext import Extension

__version__ = "0.1.1"
__author__ = "Ondřej Tůma"
__email__ = "mcbig@zeropage.cz"
__license__ = "BSD"


@contextfunction
def ctx(context):
    """Return Jinja2 context.

    See http://jinja.pocoo.org/docs/2.10/api/#the-context
    """
    return context


class TemplateInfo(object):
    """Object to store template information.

    * context - function returns Jinja Context object.
    * data - key value arguments for template render method (dict).
    * undefined - list of variables, which was not found in template.
    * template - filename of template.

    """
    def __init__(self):
        self.context = ctx
        self.data = None
        self.undefined = []
        self.template = None


class TemplateInfoExtension(Extension):
    """Jinja2 Extension which append template_info object to environment.

    >>> from jinja2 import Environment, FileSystemLoader
    >>> from jinja2_template_info import TemplateInfoExtension
    >>> data = {"title":"Title"}
    >>> env = Environment(loader=FileSystemLoader("./"),
    ...                   extensions=[TemplateInfoExtension])
    >>> env.globals["template_info"].data = data.copy()
    >>> env.globals["template_info"].template = "test.html"
    >>> template = env.get_template("test.html")
    >>> template.render(data)   # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '<!DOCTYPE html>...</html>'
    """
    def __init__(self, environment):
        super(TemplateInfoExtension, self).__init__(environment)
        info = TemplateInfo()

        class MissingUndefined(DebugUndefined):
            """Debug class for _miss_ variable in jinja."""
            def __recursion__(self, *args, **kwargs):
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

            __unicode__ = __str__   # for python2.x compatibility

        environment.undefined = MissingUndefined
        environment.globals['template_info'] = info


def render(filename, path, **kwargs):
    """Render template with some info variables.

    >>> from jinja2_template_info import render
    >>> render("test.html", "./", debug=True,
    ...        code_variable="Variable from code")
    ...        # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '<!DOCTYPE html>...</html>'
    """

    env = Environment(loader=FileSystemLoader(path))
    if kwargs.get("debug"):
        env.add_extension(TemplateInfoExtension)
        env.globals['template_info'].data = kwargs.copy()
        env.globals['template_info'].template = filename

    template = env.get_template(filename)
    return template.render(kwargs)
