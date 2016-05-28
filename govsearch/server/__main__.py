from flask import Flask, request, jsonify
from engine import SearchClient, Document, Result
import os
import json
import arrow

app = Flask(__name__)

_client = SearchClient('gov',  host = os.getenv('REDIS_HOST', 'localhost'),
                        port = int(os.getenv('REDIS_PORT', 6379)))


@app.route('/search')
def search():
    """
    Search the engine
    GET params:
    q - the search query, including "exact match"
    year_min - minimal year to limit the serch to
    year_max - maximal year to limit the search to
    gov_num - limit the search to a specific government

    :return:
    """
    q = request.args.get('q', '').encode('utf-8')

    year_min = int(request.args.get('year_min', 0))
    year_max = int(request.args.get('year_max', 0))
    gov_num = int(request.args.get('gov_num', 0))
    filters = {}
    if year_max and year_min:
        dmin = arrow.get('%s' % year_min, 'YYYY').timestamp
        dmax = arrow.get('%s' % (year_max+1), 'YYYY').timestamp - 1
        filters["date"] = (dmin, dmax)
    if gov_num:
        filters["gov_num"] = (gov_num,gov_num)

    q = request.args.get('q', '').encode('utf-8')
    res = {}
    try:
        res = _client.search(q, **filters)
    except Exception as e:
        pass
    return json.dumps(res, default=lambda o: o.__dict__, encoding='utf-8')


@app.route('/resolution/<int:year>/<int:res_num>')
def resolution(year, res_num):

    res = _client.load_document('{}_{}'.format(year, res_num))
    return json.dumps(res, default=lambda o: o.__dict__)


if __name__ == '__main__':
    app.run(port=os.getenv('PORT', 8080))