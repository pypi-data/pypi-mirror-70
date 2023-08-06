from datetime import datetime, timedelta
from Adapters.Repository.${module}Repository import ${module}Repository
from Application.Infrastructure.Exception.RuntimeException \
    import GeneralExceptionError


class ${module}sDomain:
    _DEFAULT_PAGE = 1
    _DEFAULT_PER_PAGE = 20
    _DEFAULT_DIRECTION = 'ASC'

    def __init__(self, session):
        """
        Initialises the UseCase for ${module}
        :param session:
        """
        self.session = session

    @staticmethod
    def retrieve_valid_schema():
        FIELDS = {
            'example': {
                'type': 'string',
                'required': False,
                'minlength': 2,
                'maxlength': 200
            }
        }

        return {
            'example': FIELDS['example']
        }

    def list_all(self, page, per_page,
                 from_date=None, to_date=None, direction=None):
        """
        List all instances of ${module}
        :param page:
        :param per_page:
        :param from_date:
        :param to_date:
        :param direction:
        :return:
        """
        page = page if page else self._DEFAULT_PAGE
        per_page = per_page if per_page else self._DEFAULT_PER_PAGE
        direction = direction.upper() if direction else self._DEFAULT_DIRECTION
        if from_date and to_date is None:
            to_date = datetime.now()

        return \
            ${module}Repository(self.session).list(
                page, per_page, from_date, to_date, direction)

    def load(self, uuid):
        """
        Load instances of ${module} for uuid
        :param uuid:
        :return:
        """
        return \
            ${module}Repository(self.session).load_by_uuid(uuid)

    def create(self, data):
        """
        Create a new instance of ${module}

        :param data:
        :return:
        """
        return \
            ${module}Repository(self.session).create(data)

    def update(self, uuid, data):
        """
        Updates the instance of ${module} by uuid

        :param uuid:
        :param data:
        :return:
        """
        return \
            ${module}Repository(self.session).update(uuid, data)

    def load_page_metadata(
            self, page, per_page, from_date=None,
            to_date=None):
        """

        :param page:
        :param per_page:
        :param from_date:
        :param to_date:
        :return:
        """
        page = page if page else self._DEFAULT_PAGE
        per_page = per_page if per_page else self._DEFAULT_PER_PAGE

        try:
            page_count, total = self.retrieve_page_count(
                int(per_page), from_date, to_date)

            return {
                'total_results': int(total),
                'page': int(page),
                'page_count': int(page_count),
                'per_page': int(per_page),
            }
        except Exception as e:
            raise GeneralExceptionError(e)

    def retrieve_page_count(
            self, per_page, from_date=None,
            to_date=None):
        """

        :param per_page:
        :param from_date:
        :param to_date:
        :return:
        """
        if not per_page:
            return 0

        import math
        total = ${module}Repository(self.session).count_all(
            from_date, to_date)
        return math.ceil(total / per_page), total

    @staticmethod
    def validate_date_range(date, source):
        """

        :param date:
        :param source:
        :return:
        """
        _CONTRACT_DATE_FORMAT = "%Y-%m-%d"

        try:
            if source == 'to':
                return datetime.strptime(date, _CONTRACT_DATE_FORMAT) + \
                       timedelta(days=1)
            else:
                return datetime.strptime(date, _CONTRACT_DATE_FORMAT)
        except TypeError:
            raise
        except ValueError:
            raise
        except Exception:
            raise
