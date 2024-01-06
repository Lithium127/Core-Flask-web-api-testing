from . import teams


@teams.route("/")
def teams():
    return "Teams"