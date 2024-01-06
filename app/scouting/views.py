from . import scouting


@scouting.route("/")
def index():
    return "Scouting"