# -*- coding: utf-8 -*-

import arrow
import json
import re


class ResolutionError(RuntimeError):
    """Raised when crawling resulted in unexpected results.

    e.g. multiple titles, empty bodies, etc.
    """

    pass


class ResolutionPipeline(object):
    def __init__(self):
        self.file = open("dump.json", "wb")

        # compile regular expressions:

        # input looks like 'dec14R.aspx'
        # we need the resolution number (14R)
        self.resolution_number_pattern = re.compile(r"^\D+(?P<number>.+?)\..*$")

        # input looks like 'ממשלה/הממשלה ה - 34 בנימין נתניהו;'
        # we need the government number (34) and prime minister name (בנימין נתניהו)
        self.gov_pattern = re.compile(r'^.+\s??\-\s?(?P<gov_number>.+?)\s+?(?P<pm_name>.+?);?$')

    def process_item(self, item, spider):
        try:
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
        except ResolutionError as ex:
            dump = (json.dumps({'error': repr(ex), 'url': item["url"]},
                               ensure_ascii=False)
                    .encode("utf8"))
        else:
            # encode to utf-8 and dump to file
            dump = json.dumps(data, ensure_ascii=False).encode("utf8")

        self.file.write(dump + "\n")

        return item

    # the following are specific field handling functions
    # e.g. cleaning, stripping, etc.
    # these should be called before dumping the data

    def get_date(self, item):
        if len(item["date"]) != 1:
            raise ResolutionError("Date field length is not 1 for item %s", item)
        return arrow.get(item["date"][0], "YYYYMMDD")

    def get_resolution_number(self, item):
        if len(item["resolution_number"]) != 1:
            raise ResolutionError("Resolution number field length is not 1 for item %s", item)
        return self.resolution_number_pattern.search(item["resolution_number"][0]).group('number')

    def get_gov_number(self, item):
        if len(item["gov"]) != 1:
            raise ResolutionError("Government field length is not 1 for item %s", item)
        gov_match = self.gov_pattern.search(item["gov"][0])
        return gov_match.group("gov_number")

    def get_pm_name(self, item):
        if len(item["gov"]) != 1:
            raise ResolutionError("Government field length is not 1 for item %s", item)
        gov_match = self.gov_pattern.search(item["gov"][0])
        return gov_match.group("pm_name")

    def get_title(self, item):
        if len(item["title"]) == 0:
            raise ResolutionError("Title fields is empty for item %s", item)
        return '\n'.join(item["title"]).strip()

    def get_subject(self, item):
        if len(item["subject"]) == 0:
            raise ResolutionError("Subject field is empty for item %s", item)
        return '\n'.join(item["subject"]).strip()

    def get_body(self, item):
        if len(item["body"]) == 0:
            raise ResolutionError("Body field is empty for item %s", item)
        return '\n'.join(item["body"]).strip()
