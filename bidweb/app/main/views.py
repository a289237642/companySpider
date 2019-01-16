#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from flask_login import current_user, login_required

from . import main


@main.route('/')
# @login_required
def home():
    print(current_user)

    # is_authenticated()
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    else:
        return redirect(url_for("auth.login"))


@main.route("/index")
@login_required
def index():
    return render_template("index.html")
