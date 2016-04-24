# -*- coding: utf-8 -*-
from invoke import run, task
from invoke.util import cd


@task
def install_deps():
    run("pip install -t ./src -r requirements.txt")


@task(install_deps)
def build():
    with cd('src'):
        run("zip ../Mianliao.alfredworkflow ./ -r --exclude=*.DS_Store* --exclude=*.pyc* --exclude=*.gitignore* --exclude=*.dist-info*")


@task(build)
def install():
    run("open Mianliao.alfredworkflow")