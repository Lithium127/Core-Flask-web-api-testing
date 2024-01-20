from flask import render_template

from . import site_info


@site_info.route("/about")
def about():
    return render_template("about.html")