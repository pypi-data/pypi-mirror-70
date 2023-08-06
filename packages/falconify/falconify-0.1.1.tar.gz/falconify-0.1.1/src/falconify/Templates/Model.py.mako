from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from Adapters.SqlAlchemy.Model.Base import Base
from Adapters.SqlAlchemy import Alchemy


class ${module}(Base):

    def __call__(self, *args, **kwargs):
        return "<${module}(id='%s', " \
               "uuid='%s')>" % \
               (
                   self.id,
                   self.uuid,
               )

    FIELDS = {
        'uuid': str
    }
