# -*- coding: utf-8 -*-

import json


class DecisionPipeline(object):

    def __init__(self):
        self.file = open("dump.json", "wb")

    def process_item(self, item, spider):
        decision = json.dumps(dict(item) + "\n")
        self.file.write(decision)
        return item
