# -*- coding: utf-8 -*-
import json
import click
import sys
print sys.path
from engine import SearchClient, Item

@click.command()
@click.option('--file', help='File to import')
@click.option('--host', default='localhost', help='Redis host to push to')
@click.option('--port', default=6379, help='Redis port to push to')
@click.option('--index', default='gov', help='Search index')
@click.option('--drop', is_flag=True, help='Do we drop the index before updating it?')
def import_file(file, host, port, index, drop):
    print file
    client = SearchClient(index, host=host, port=port)
    if drop:
        client.drop_index()

    Item.create_index(client)
    for line in open(file):
        obj = {k: v.encode('utf-8') if isinstance(v, unicode) else v
               for k,v in json.loads(line, encoding='utf-8').iteritems()}

        item = Item(**obj)
        item.index(client)

    print client.search("נתניהו")

if __name__ == '__main__':
    import_file()



