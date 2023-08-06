class ${module}Transformer:
    def __init__(self):
        pass

    def transform(self, data, method):
        """

        :param data:
        :param method:
        :return:
        """
        if method == 'POST':
            return self._fulfill_post_contract(data)
        elif method == 'GET':
            return self._fulfill_get_contract(data)
        elif method == 'PUT':
            return self._fulfill_put_contract(data)
        else:
            return data

    def _fulfill_post_contract(self, data):
        """

        :param data:
        :return:
        """
        return {
            'uuid': str(data)
        }

    def _fulfill_get_contract(self, data):
        """

        :param data:
        :return:
        """

        result = []
        if isinstance(data, list):
            for item in data:
                result.append({
                    "uuid": str(item.uuid),
                    "is_active": item.is_active,
                    "created": str(item.created),
                    "modified": str(item.modified)
                })
        else:
            item = data
            result.append({
                "uuid": str(item.uuid),
                "is_active": item.is_active,
                "created": str(item.created),
                "modified": str(item.modified)
            })

        return result

    def _fulfill_put_contract(self, data):
        """

        :param data:
        :return:
        """
        return {
            'uuid': str(data)
        }
