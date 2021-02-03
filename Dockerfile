# vim: ft=dockerfile
# docker build -t jinja2-template-info .
# docker run -ti --rm -w "$PWD" -v "$PWD:$PWD" jinja2-template-info bash

FROM python:3.6-buster

RUN pip3 install --find-links=file:///tmp \
        pytest pytest-pylint pytest-doctestplus jinja2 importlib_resources

ENV LC_ALL C.UTF-8
