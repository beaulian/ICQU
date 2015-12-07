# coding=utf-8

from flask import render_template, make_response
from . import main


@main.route("/", methods=["GET"])
def index():
	return render_template("main/index.html")


@main.route("/xiaoche", methods=["GET"])
def xiaoche():
	return render_template("main/xiaoche.html")


@main.route("/xiaoli", methods=["GET"])
def xiaoli():
	return render_template("main/xiaoli.html")


@main.route("/lib", methods=["GET"])
def lib():
	return render_template("main/lib.html")


@main.route("/kard", methods=["GET"])
def kard():
	return render_template("main/kard.html")


@main.route("/repair", methods=["GET"])
def repair():
	return render_template("main/repair.html")

@main.route("/kebiao", methods=["GET"])
def kebiao():
	return render_template("main/kebiao.html")


@main.route("/grade", methods=["GET"])
def grade():
	return render_template("main/grade.html")


@main.route("/person", methods=["GET"])
def person():
	return render_template("main/person.html")