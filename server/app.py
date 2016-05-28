#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, json
from flask.json import JSONEncoder
from engine.models import SearchClient, Document, Result
import os
import json
import arrow

app = Flask(__name__)

class CustomJSONEncoder(JSONEncoder):
    def __init__(self, **kwargs):
        kwargs.update({
            "ensure_ascii": False,
            "encoding": "utf-8",
        })

        super(CustomJSONEncoder, self).__init__(**kwargs)

    def default(self, obj):
        return obj.__dict__

# app.json_encoder = CustomJSONEncoder


# redis search client
_client = SearchClient('gov',  host = os.getenv('REDIS_HOST', 'localhost'),
                       port = int(os.getenv('REDIS_PORT', 6379)))


@app.route('/search')
def search():
    """Perform a search via search engine.

    GET params:
    q: the search query, including "exact match"
    year_min: minimum year to limit the search to
    year_max: maximum year to limit the search to
    gov_num: limit search to a specific government
    """
    # search filters
    year_min = int(request.args.get('year_min', 0))
    year_max = int(request.args.get('year_max', 0))
    gov_num = int(request.args.get('gov_num', 0))

    # pagination
    results_from = int(request.args.get('results_from', 0))
    results_size = int(request.args.get('results_size', 20))

    filters = {}

    if year_max and year_min:
        dmin = arrow.get('%s' % year_min, 'YYYY').timestamp
        dmax = arrow.get('%s' % (year_max+1), 'YYYY').timestamp - 1
        filters["date"] = (dmin, dmax)

    if gov_num:
        filters["gov_num"] = (gov_num, gov_num)

    query = request.args.get('q', '').encode('utf-8')
    res = _client.search(query, results_from=results_from, results_size=results_size, **filters)

    return json.dumps(res, default=lambda o: o.__dict__, encoding='utf-8')
# return json.dumps(res)


@app.route('/resolution/<int:year>/<int:resolution_number>')
def resolution(year, resolution_number):
    """Return specific resolution according to its number and year."""
    res = _client.load_document('{}_{}'.format(year, resolution_number))
    return json.dumps(res, default=lambda o: o.__dict__)
# return json.dumps(res)


if __name__ == '__main__':
    app.run(
        port=os.getenv('PORT', 8080),
        debug=os.getenv('DEBUG', False),
    )
