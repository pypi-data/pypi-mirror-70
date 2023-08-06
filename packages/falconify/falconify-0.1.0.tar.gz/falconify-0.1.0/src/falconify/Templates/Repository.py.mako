from Adapters.SqlAlchemy.Model.Base import Base
from Domain.Model.${module} import ${module}
from sqlalchemy.exc import DataError
from Application.Infrastructure.Exception.RuntimeException \
    import GeneralExceptionError
from Application.Infrastructure.Exception.RuntimeException \
    import InvalidParameterError
import uuid


class ${module}Repository(Base):

    def __init__(self, session):
        """
        Initialises the repository for a ${module} class
        :param session: object
        """
        self.session = session

    def list(self, page, per_page, from_date, to_date,
             direction):
        """
        List all the instances of a ${module}
        :param page:
        :param per_page:
        :param from_date:
        :param to_date:
        :param direction:
        :return:
        """
        try:
            query = self.session.query(${module})

            if from_date:
                query = query.filter(${module}.created > from_date)

            if to_date:
                query = query.filter(${module}.created < to_date)

            if direction == 'ASC':
                query = query.order_by(${module}.id.asc())
            else:
                query = query.order_by(${module}.id.desc())

            query = query.limit(per_page).offset(
                int(per_page) * (int(page) - 1))

            return query.all()
        except Exception as e:
            raise GeneralExceptionError(
                "{}".format(type(e)))

    def load_by_uuid(self, uuid):
        """
        Loads an instance of a ${module} by uuid

        :param uuid: uuid
        :return: SqlAlchemy object
        """
        try:
            return self.session.query(${module}) \
                .filter(${module}.uuid == uuid)\
                .first()
        except DataError as e:
            raise InvalidParameterError(str(e.orig))
        except Exception as e:
            raise GeneralExceptionError(
                "{} - for {}".format(type(e), uuid))

    def create(self, data):
        """
        Creates a new instance a ${module}

        :param data: object
        """
        entity = ${module}()

        try:
            entity.uuid = uuid.uuid4()

            self.session.add(entity)
            self.session.commit()

            return entity.uuid

        except Exception as e:
            raise GeneralExceptionError(
                "{}".format(type(e)))

    def update(self, uuid, data):
        """
        Updates the entity of a ${module} loaded by uuid

        :param uuid: uuid
        :param data: object
        :return:
        """

        entity = self.load_by_uuid(uuid)

        try:
            if 'name' in data:
                entity.name = data['name']

            self.session.commit()

            return entity.uuid
        except Exception as e:
            raise GeneralExceptionError(
                "{}".format(type(e)))

    def retrieve_internal_id_for_entity(self, uuid):
        """
        Retrieves the internal id for an entity of ${module} loaded by uuid

        :param uuid:
        :return:
        """
        try:
            entity = self.load_by_uuid(uuid)

            if not entity:
                raise InvalidParameterError('Entity Not Found %s' % uuid)

            return entity.id
        except DataError as e:
            raise InvalidParameterError(str(e.orig))
        except Exception as e:
            raise GeneralExceptionError(
                "{} - for {}".format(str(e.__dict__), uuid))

    def count_all(self, from_date, to_date):
        """
        Count all records for set query

        :param from_date:
        :param to_date:
        :return:
        """
        try:
            query = self.session.query(${module})
            if from_date is not None:
                query = query.filter(${module}.created > from_date)

            if to_date is not None:
                query = query.filter(${module}.created < to_date)

            return query.count()
        except Exception as e:
            raise GeneralExceptionError(
                "{}".format(type(e)))
