import functools
import datetime
import json

obj_to_json = functools.partial(json.dumps,
                                default=lambda o: o.__str__() if isinstance(o, datetime.date) else o.__dict__,
                                sort_keys=True, ensure_ascii=False)
