from falcon.util.uri import parse_query_string
from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator, ValidationError
from Application.Infrastructure.Port.Transformer.BaseTransformer \
    import BaseTransformer
from Application.Infrastructure.Exception.RuntimeException \
    import InvalidParameterError
from Domain.UseCases.${module} import ${module}sDomain


class ${module}CommandHandler:

    def __init__(self, req, res):
        self.req = req
        self.res = res
        self.session = req.context['session']

    def list(self):
        """
        List all the instances of ${module}
        :return:
        """
        page = None
        per_page = None
        from_date = None
        to_date = None
        direction = None

        qry_str = parse_query_string(self.req.query_string)

        try:
            if 'page' in qry_str:
                page = qry_str['page']

            if 'per_page' in qry_str:
                per_page = qry_str['per_page']

            if 'direction' in qry_str:
                direction = qry_str['direction']

            if 'from_date' in qry_str:
                try:
                    from_date = ${module}sDomain.validate_date_range(
                        qry_str['from_date'], 'from')
                except ValueError:
                    raise InvalidParameterError(
                        'The from date provided is not in the correct format.')
            if 'to_date' in qry_str:
                try:
                    to_date = ${module}sDomain.validate_date_range(
                        qry_str['to_date'], 'to')
                except ValueError:
                    raise InvalidParameterError(
                        'The to_date provided is not in the correct format.')

            if from_date is not None and to_date is not None:
                if from_date > to_date:
                    raise InvalidParameterError(
                        'The date range provided is out of range.')

            return ${module}sDomain(self.session).list_all(
                page,
                per_page,
                from_date,
                to_date,
                direction
            ), ${module}sDomain(self.session).load_page_metadata(
                page,
                per_page,
                from_date,
                to_date
            )
        except NoResultFound:
            return BaseTransformer().not_found()

    def load(self, uuid):
        """
        Loads an entity of ${module} by uuid

        :param uuid: uuid
        :return:
        """
        try:
            return ${module}sDomain(self.session).load(uuid)
        except NoResultFound:
            raise NoResultFound()

    def create(self):
        """
        Creates an instance of the ${module}

        :return:
        :rtype:
        """

        schema = ${module}sDomain.retrieve_valid_schema()

        # validate payload against schema retrieved from the domain
        v = Validator(schema)

        try:
            if not v.validate(self.req.context['data']):
                raise InvalidParameterError(v.errors)
        except ValidationError:
            raise InvalidParameterError(
                'Invalid Request %s' % self.req.context)

        return ${module}sDomain(self.session). \
            create(self.req.context['data'])

    def update(self, uuid):
        """
        Updates the instance of ${module} by uuid
        :param uuid: uuid
        :return:
        """
        return \
            ${module}sDomain(self.session).update(
                uuid, self.req.context['data'])
