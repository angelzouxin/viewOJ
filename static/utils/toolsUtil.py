import functools
import json


obj_to_json = functools.partial(json.dumps, default=lambda o: o.__dict__, sort_keys=True, ensure_ascii=False)
