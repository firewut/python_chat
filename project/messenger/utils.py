import string
import random
import datetime


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def json_serial(obj):
    """
    json.dumps(self.as_dict(), default=utils.json_serial)
    """
    return obj.isoformat() if obj != None and hasattr(obj, 'isoformat') else obj
