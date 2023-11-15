from abc import ABC, abstractmethod
from typing import List, Union
from resource import Resources

class ParseRule(ABC):

    def __init__(self,tag):
        self.tag = tag
    
    @abstractmethod
    def parse(self, response):
        pass

    def get_tag_contents(self, response):
        start_index, end_index, length = self.get_tag_indices(response)
        contents = response[start_index+length:end_index]
        return contents 

    def get_tag_indices(self, response):
        start_index = response.find(f"<{self.tag}>")
        end_index = response.find(f"</{self.tag}>")
        return start_index, end_index, len(f"<{self.tag}>")

class UnformattedParseRule(ParseRule):
    def parse(self, response):
        return self.get_tag_contents(response)

class ResourcesParseRule(ParseRule):
    def parse(self, response):
        contents = self.get_tag_contents(response)
        return Resources(contents)


class Parser:

    def __init__(self, parse_rules: List[ParseRule] = None):
        if parse_rules is None:
            parse_rules = []
        self.parse_rules = parse_rules
    
    def add_parse_rules(self, parse_rules: Union[List[ParseRule], ParseRule]):
        if isinstance(parse_rules, ParseRule):
            parse_rules = [parse_rules]
        self.parse_rules += parse_rules

    def parse(self, response):
        return {rule.tag: rule.parse(response) for rule in self.parse_rules}