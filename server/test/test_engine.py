# -*- coding: utf-8 -*-
from engine import SearchClient
import unittest


class EngineTestCase(unittest.TestCase):

    def testEngine(self):

        client = SearchClient('testung')
        client.drop_index()
        client.create_index(title=10, body=1, foo=client.NUMERIC)

        client.add_document(doc_id="doc1", title="hello world",
                            body="foo bar hello", foo=1)
        client.add_document(
            doc_id="doc2", title="hello my world", body="foo bar helloz", foo=2)

        res = client.search("hello world")

        self.assertEqual(2, res.total)
        self.assertEqual(2, len(res.docs))
        print res.docs

        res = client.search('hello', foo=(0, 1))
        self.assertEqual(1, res.total)
        self.assertEqual(1, len(res.docs))

        res = client.search('hello', fields=['body'])
        self.assertEqual(1, res.total)
        self.assertEqual(1, len(res.docs))

if __name__ == "__main__":
    unittest.main()
