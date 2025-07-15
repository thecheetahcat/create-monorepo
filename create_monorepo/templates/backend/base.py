BASE = """from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class Mixins:
    def to_dict(self):
        mapper = inspect(self).mapper
        return {attr.key: getattr(self, attr.key) for attr in mapper.column_attrs}


class Base(Mixins, DeclarativeBase):
    pass
"""
