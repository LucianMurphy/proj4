"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request: {}".format(request.args))
    km = request.args.get('km', type=float)
    brevet_dist = request.args.get('brevet_dist_km', 200, type = int)
    begin_date = request.args.get('begin_date', '2017-01-01')
    begin_time = request.args.get('begin_time', '00:00')
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    if km is None:
        return flask.jsonify(result ={"error": "Distance must be a number"})
    try:
        start = arrow.get("{} {}".format(begin_date, begin_time), "YYYY-MM-DD HH:mm")
        result = {
            "open": acp_times.open_time(km, brevet_dist, start.isoformat()),
            "close": acp_times.close_time(km, brevet_dist, start.isoformat()),
        }
    except (ValueError, arrow.parser.ParserError) as err:
        result = {"error": str(err)}
    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
