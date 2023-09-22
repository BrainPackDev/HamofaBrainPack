from odoo.http import JsonRPCDispatcher,SessionExpiredException,serialize_exception
from werkzeug.exceptions import (NotFound)

class JsonRPCDispatcherExtend(JsonRPCDispatcher):

    def handle_error(self, exc: Exception):
        # OVERRIDE BASE METHOD
        error = {
            'code': 200,
            'message': "BrainPack Server Error",
            'data': serialize_exception(exc),
        }
        if isinstance(exc, NotFound):
            error['code'] = 404
            error['message'] = "404: Not Found"
        elif isinstance(exc, SessionExpiredException):
            error['code'] = 100
            error['message'] = "Odoo Session Expired"

        return self._response(error=error)


