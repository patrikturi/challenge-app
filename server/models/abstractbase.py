from sqlalchemy import inspect

from server import database
from server.database import Base


class AbstractBase(Base):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = database.session

    def asdict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        name = self.__class__.__name__
        props = ', '.join([f'{key}={value}' for key, value in sorted(self.asdict().items())])
        return f'<{name}({props})>'
