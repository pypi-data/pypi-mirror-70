import falcon
from Application.Infrastructure.Port.Base \
    import BaseResource
from Application.Infrastructure.Middleware.Hooks.Auth \
    import auth_required
from Application.Features.${module}.${module}CommandHandler \
    import ${module}CommandHandler
from Application.Infrastructure.Port.Transformer.${module}Transformer \
    import ${module}Transformer


class ${module}CollectionRequestHandler(BaseResource):

    @falcon.before(auth_required)
    def on_get(self, req, res):
        """
        Receives the command to fetch all ${module}
        from the collection

        :param req:
        :param res:
        :return:
        """
        try:
            qry, pagination_meta = ${module}CommandHandler(req, res).list()
            contract_response = ${module}Transformer()\
                .transform(qry, req.method)
            self.on_success(res, contract_response,
                            pagination_meta=pagination_meta)
        except TypeError as e:
            self.on_error(res, e)

    @falcon.before(auth_required)
    def on_post(self, req, res):
        """
        Creates a new entity of ${module}

        :param req:
        :param res:
        :return:
        """
        try:
            cmd = ${module}CommandHandler(req, res).create()
            contract_response = ${module}Transformer()\
                .transform(cmd, req.method)
            self.on_success(res, contract_response)
        except TypeError as e:
            self.on_error(res, e)


class ${module}ItemRequestHandler(BaseResource):

    @falcon.before(auth_required)
    def on_get(self, req, res, uuid):
        """
        List an entity of ${module} by uuid
        :param req:
        :param res:
        :param uuid: uuid
        :return:
        """
        try:
            cmd = ${module}CommandHandler(req, res).load(uuid)
            contract_response = ${module}Transformer()\
                .transform(cmd, req.method)
            self.on_success(res, contract_response)
        except TypeError as e:
            self.on_error(res, e)

    @falcon.before(auth_required)
    def on_put(self, req, res, uuid):
        """
        Updates the entity of ${module} loaded by uuid

        :param req:
        :param res:
        :param uuid:
        :return:
        """
        try:
            cmd = ${module}CommandHandler(req, res).update(uuid)
            contract_response = ${module}Transformer()\
                .transform(cmd, req.method)
            self.on_success(res, contract_response)
        except TypeError as e:
            self.on_error(res, e)
