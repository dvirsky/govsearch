from redis import Redis, RedisError, ConnectionPool
import datetime

class Item(object):

    def __init__(self, title, url, subject, body, date, number, government):

        dt = datetime.datetime.fromtimestamp(date)

        self.id = '{}/{}'.format(dt.year, number)
        self.title = title
        self.url = url
        self.subject = subject
        self.body = body
        self.date = date
        self.number = number
        self.government = government


class Document(object):

    def __init__(self, id, **fields):

        self.id = id
        for k,v in fields.iteritems():
            setattr(self, k, v)


class Result(object):

    def __init__(self, res, hascontent):

        self.total = res[0]
        self.docs = []
        for i in xrange(1, len(res), 2 if hascontent else 1):
            id = res[i]
            fields = dict(res[i+1]) if hascontent else {}
            self.docs.append(Document(id, **fields))

class SearchClient(object):

    NUMERIC = 'numeric'

    CREATE_CMD = 'FT.CREATE'
    SEARCH_CMD = 'FT.SEARCH'
    ADD_CMD = 'FT.ADD'
    DROP_CMD = 'FT.DROP'

    def __init__(self, index_name, host='localhost', port=6379):
        self.host = host
        self.port = port
        self.index_name = index_name

        self.redis = Redis(connection_pool=ConnectionPool(host=host, port=port))

    def create_index(self, **fields):
        """
        Create the search index. Creating an existing index juts updates its properties
        :param fields: a kwargs consisting of field=[score|NUMERIC]
        :return:
        """
        self.redis.execute_command(self.CREATE_CMD, self.index_name, *fields.items())

    def drop_index(self):
        """
        Drop the index if it exists
        :return:
        """
        self.redis.execute_command(self.DROP_CMD, self.index_name)

    def add_document(self, **fields):
        pass

    def search(self, query, no_content = False, fields=None, **filters):
        """
        Search eht
        :param query:
        :param fields:
        :param filters:
        :return:
        """

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
        print args

        res = self.redis.execute_command(self.SEARCH_CMD, *args)

        return Result(res, not no_content)

