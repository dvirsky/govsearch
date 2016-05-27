# -*- coding: utf-8 -*-

import arrow
import json
import re


class ResolutionPipeline(object):
    def __init__(self):
        self.file = open("dump.json", "wb")

        # compile regular expressions:

        # input looks like 'dec1495.aspx'
        # we need the resolution number (1495)
        self.resolution_number_pattern = re.compile(r"^\D+(?P<number>\d+?)\..*$")

        # input looks like 'ממשלה/הממשלה ה - 34 בנימין נתניהו;'
        # we need the government number (34) and prime minister name (בנימין נתניהו)
        self.gov_pattern = re.compile(r'^.+\s??\-\s?(?P<gov_number>.+?)\s+?(?P<pm_name>.+?);?$')

    def process_item(self, item, spider):
        data = {
            'url': item["url"],
            'date': self.get_date(item).timestamp,
            'resolution_number': self.get_resolution_number(item),
            'gov_number': self.get_gov_number(item),
            'pm_name': self.get_pm_name(item),
            'title': self.get_title(item),
            'subject': self.get_subject(item),
            'body': self.get_body(item),
        }

        # encode to utf-8 and dump to file
        resolution = json.dumps(data, ensure_ascii=False).encode("utf8")
        self.file.write(resolution + "\n")

        return item

    # the following are specific field handling functions
    # e.g. cleaning, stripping, etc.
    # these should be called before dumping the data

    def get_date(self, item):
        if len(item["date"]) != 1:
            raise RuntimeError("Date field length is not 1 for item %s", item)
        return arrow.get(item["date"][0], "YYYYMMDD")

    def get_resolution_number(self, item):
        if len(item["resolution_number"]) != 1:
            raise RuntimeError("Resolution number field length is not 1 for item %s", item)
        return self.resolution_number_pattern.search(item["resolution_number"][0]).group('number')

    def get_gov_number(self, item):
        if len(item["gov"]) != 1:
            raise RuntimeError("Government field length is not 1 for item %s", item)
        gov_match = self.gov_pattern.search(item["gov"][0])
        return gov_match.group("gov_number")

    def get_pm_name(self, item):
        if len(item["gov"]) != 1:
            raise RuntimeError("Government field length is not 1 for item %s", item)
        gov_match = self.gov_pattern.search(item["gov"][0])
        return gov_match.group("pm_name")

    def get_title(self, item):
        if len(item["title"]) == 0:
            raise RuntimeError("Title fields is empty for item %s", item)
        return ''.join(item["title"]).strip()

    def get_subject(self, item):
        if len(item["subject"]) == 0:
            raise RuntimeError("Subject field is empty for item %s", item)
        return ''.join(item["subject"]).strip()

    def get_body(self, item):
        if len(item["body"]) == 0:
            raise RuntimeError("Body field is empty for item %s", item)
        return ''.join(item["body"]).strip()
