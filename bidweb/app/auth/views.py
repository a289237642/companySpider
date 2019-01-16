#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from sqlalchemy.exc import OperationalError, ProgrammingError

from . import auth
from .forms import LoginForm
from app.modles import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    # form = LoginForm(csrf_enabled=False)
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                user = User.query.filter_by(username=form.username.data).first()
            except (OperationalError, ProgrammingError) as e:
                print(str(e))
                flash("数据库连接错误")
                return redirect(url_for("auth.login"))

            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get("next") or url_for("main.index"))
            else:
                flash("认证失败")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            flash("请检查您的用户名或密码")
            return redirect(url_for("auth.login"))
    return render_template("login.html", form=form, next=None)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('您已经登出系统')
    return redirect(url_for('auth.login'))

