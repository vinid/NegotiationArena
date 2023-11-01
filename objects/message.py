
import json
import logging
from dataclasses import dataclass
from collections import defaultdict
@dataclass


class Message:
    data: dict = None

    def __getitem__(self, key):
        return self.data[key]

    def __str__(self):
        res = [f"'{k}': {str(v)}" for k, v in self.data.items()]
        return "{" +  ", ".join(res) + "}"


