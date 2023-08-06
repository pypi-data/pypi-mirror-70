# py_todict

## Usage
~~~~
from enum import Enum
import json

from to_dict import Dictable

class E(Enum):
    test = 'test_val'

class D:
    def __init__(self):
        self.val = 'str_val'

class C:
    def __init__(self):
        self.d1 = D()
        self.d2 = D()

class B(Dictable):
    def __init__(self, vals: list):
        self.vals = vals

class A(Dictable):
    def __init__(self):
        self.a = 5
        self.b = 'b'
        self.c = E.test
        self.d = C()
        self.e = [B([996, 997]), B([998, 999])]
        self.f = {'key_1': B([996, 997]), 'key_2': B([998, 999])}

print(A().dict)
# Outputs: {'a': 5, 'b': 'b', 'c': <E.test: 'test_val'>, 'd': <__main__.C object at 0x102afa1d0>, 'e': [{'vals': [996, 997]}, {'vals': [998, 999]}], 'f': {'key_1': {'vals': [996, 997]}, 'key_2': {'vals': [998, 999]}}}

print(json.dumps(A().json, indent=4))
# Outputs: 
# {
#     "a": 5,
#     "b": "b",
#     "c": "test_val",
#     "d": {
#         "d1": {
#             "val": "str_val"
#         },
#         "d2": {
#             "val": "str_val"
#         }
#     },
#     "e": [
#         {
#             "vals": [
#                 996,
#                 997
#             ]
#         },
#         {
#             "vals": [
#                 998,
#                 999
#             ]
#         }
#     ],
#     "f": {
#         "key_1": {
#             "vals": [
#                 996,
#                 997
#             ]
#         },
#         "key_2": {
#             "vals": [
#                 998,
#                 999
#             ]
#         }
#     }
# }
~~~~