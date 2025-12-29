from django.db import connections
from django.db.utils import OperationalError

def check_database_health() -> bool:
    try:
        with connections["default"].cursor():
            return True
    except OperationalError:
        return False