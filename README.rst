Jinja2 template info
====================

Jinja2-template_info is Jinja2 Extension module and piece of code to generate
and show some template information which could help with debuging templates.

``template_info``
-----------------

``render(template, path, **kwargs)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
That is simple function, which return rendered string from Jinja2. If there is
``debug`` variable set to positive variable in ``kawrgs``,
``TemplateInfoExtension`` is used and attributes ``data`` and ``template`` was
set.

:template: template file name
:path: path or paths, where jinja could find the template
:\**kwargs: data, which are send to template


.. code:: python

    >>> from jinja2_template_info import render
    >>> render("test.html", "./", debug=True,
    ...        code_variable="Variable from code")
    ...        # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
    '<!DOCTYPE html>...</html>'


``class TemplateInfoExtension(Extension)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Extension class, which append ``TemplateInfo`` instance to template in
``template_info`` variable. This class contains own ``Undefined`` class, which
is use to store undefined variables names. They are in
``template_info.undefined``.

.. code:: python

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

``template_info.html``
----------------------
This file contains some macros for better html output of variables. Becouse
local template variables are readed only from each template, that must be
used as macro argument.

``render_info(local_variables=none)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Append debug output to template. Output is labeled with section name, some
sections are shown only if they are set.

:Local Variables:
            Variables from template, where render_info is call. Local
            variable could be get with
            ``template_info.context().get_exported())`` call.
:Template:  Template file name (``template_info`` variable).
:Input Variables:
            kwargs data from ``render`` function (``template_info`` variable).
:Context:   Context content without variables. There are all functions, macros
            and other objects set to ``environment.globals``.
:Undefined objects:
            List of undefined variables,functions, macros and other objects,
            which is not found and template want use it.