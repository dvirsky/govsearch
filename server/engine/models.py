# -*- coding: utf-8 -*-
from datetime import datetime
import itertools
import json
import time
from redis import Redis, ConnectionPool


class ImportDocument(object):
    """Represents a document about to be inserted into the database."""
    def __init__(self, title, url, subject, body, date, resolution_number, gov_number, pm_name):
        year = datetime.fromtimestamp(date).year
        self.id = '{}_{}'.format(year, resolution_number)

        self.title = title
        self.url = url
        self.subject = subject
        self.body = body
        self.date = date
        self.resolution_number = resolution_number
        self.gov_number = gov_number
        self.pm_name = pm_name

    @staticmethod
    def create_index(client):
        client.create_index(
            title=10.0,
            url=1.0,
            subject=5.0,
            body=1.0,
            pm_name=5.0,
            gov_number=client.NUMERIC,
            date=client.NUMERIC,
            resolution_number=client.NUMERIC,
        )

    @staticmethod
    def fromJSON(jstr):
        obj = json.loads(jstr)
        return ImportDocument(**obj)

    def index(self, client):
        client.add_document(doc_id=self.id, score=1.0, **self.__dict__)


class Document(object):
    """Represents a Redisearch document."""
    def __init__(self, id, **fields):
        self.id = id
        for k, v in fields.iteritems():
            setattr(self, k, v)

    def snippetize(self, field, length=500, boldTokens=[]):
        """Shorten document given field text if too long."""
        txt = getattr(self, field, '')
        for tok in boldTokens:
            txt = txt.replace(tok, "<b>%s</b>" % tok)

        while length < len(txt) and txt[length] != ' ':
            length += 1

        setattr(self,
                field,
                (txt[:length] + '...') if len(txt) > length else txt)

    def __repr__(self):
        return 'Document %s' % self.__dict__


class Result(object):
    """Represents a search result."""
    def __init__(self, res, hascontent, queryText, duration=0):
        self.total = res[0]
        self.duration = duration
        self.docs = []

        tokens = filter(None, queryText.rstrip("\" ").lstrip(" \"").split(' '))
        for i in xrange(1, len(res), 2 if hascontent else 1):
            id = res[i]
            fields = (dict(dict(itertools.izip(res[i + 1][::2], res[i + 1][1::2])))
                      if hascontent
                      else {})
            try:
                del fields['id']
            except KeyError:
                pass

            doc = Document(id, **fields)
            try:
                doc.snippetize('body', length=500, boldTokens=tokens)
            except Exception as e:
                print repr(e)

            self.docs.append(doc)

    def __repr__(self):
        return 'Result{%d total, docs: %s}' % (self.total, self.docs)


class SearchClient(object):
    """Redisearch client."""

    # redisearch statements
    NUMERIC = 'numeric'

    CREATE_CMD = 'FT.CREATE'
    SEARCH_CMD = 'FT.SEARCH'
    ADD_CMD = 'FT.ADD'
    DROP_CMD = 'FT.DROP'

    def __init__(self, index_name, host='localhost', port=6379):
        self.host = host
        self.port = port
        self.index_name = index_name

        self.redis = Redis(
            connection_pool=ConnectionPool(host=host, port=port))

    def create_index(self, **fields):
        """Create/Update search index.

        NOTE creating an existing index juts updates its properties.

        fields: a kwargs consisting of field=[score|NUMERIC]
        """
        self.redis.execute_command(
            self.CREATE_CMD, self.index_name, *itertools.chain(*fields.items()))

    def drop_index(self):
        """Drop the index if exists."""
        self.redis.execute_command(self.DROP_CMD, self.index_name)

    def add_document(self, doc_id, score=1.0, **fields):
        args = ([self.ADD_CMD, self.index_name, doc_id, score, 'FIELDS'] +
                list(itertools.chain(*fields.items())))

        self.redis.execute_command(*args)

    def load_document(self, id):
        fields = self.redis.hgetall(id)
        try:
            del fields['id']
        except KeyError:
            pass

        return Document(id=id, **fields)

    def search(self, query, results_from=0, results_size=10, no_content=False, fields=None, **filters):
        args = [self.index_name, query]
        if no_content:
            args.append('NOCONTENT')

        if fields:
            args.append('INFIELDS')
            args.append(len(fields))
            args += fields

        if filters:
            for k, v in filters.iteritems():
                args += ['FILTER', k] + list(v)

        args += ["LIMIT", results_from, results_size]
        print args

        start = time.time()
        res = self.redis.execute_command(self.SEARCH_CMD, *args)
        diff = time.time() - start

        return Result(res, not no_content, queryText=query, duration=diff*1000.0)
