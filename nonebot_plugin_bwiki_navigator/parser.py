from html.parser import HTMLParser
from typing import Union, Tuple, List


class SimpleInnerParser(HTMLParser):
    def __init__(self, target_tag='p', target_attr: Union[str, Tuple, List[Tuple]] = None, text_context=True):
        super().__init__()
        self.output = []
        self.open_write = False
        self.target_tag = target_tag
        self.target_attr = target_attr
        self.text_context = text_context

    def handle_starttag(self, tag, attrs):
        if tag == self.target_tag or not self.target_tag:
            checker = get_from_attrs(attrs, self.target_attr) if self.target_attr else True
            self.open_write = True and checker
        if value := get_from_attrs(attrs, self.target_attr):
            if not self.text_context:
                self.output.append(str(value).strip())
                self.open_write = False

    def handle_endtag(self, tag):
        if tag == self.target_tag:
            self.open_write = False

    def handle_data(self, data: str):
        if self.open_write and self.text_context and data.strip():
            self.output.append(data.strip())


def get_from_attrs(attr_list, target):
    if not target:
        return False
    if isinstance(target, str):
        for attr in attr_list:
            if target == attr[0]:
                return attr[1]
    if isinstance(target, tuple):
        for attr in attr_list:
            if target[0] == attr[0] and target[1] in attr[1]:
                return True
    if isinstance(target, list) and len(target) == 2:
        find = target[0]
        fetch = target[1]
        got = False
        temp = None
        for attr in attr_list:
            if find[0] == attr[0] and find[1] in attr[1]:
                got = True
            if fetch[0] == attr[0]:
                temp = attr[1]
            if temp and got:
                return temp
    return False
