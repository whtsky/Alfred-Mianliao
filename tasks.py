# -*- coding: utf-8 -*-
from invoke import run, task


@task
def install():
    run("pip install -t ./src -r requirements.txt")
