from . import scouting



@scouting.route("/")
def index():
    return "Scouting"


# API endpoint for sending data to.
@scouting.route("/report", methods=["GET", "POST"])
def report():
    return "Scouting Post request"
