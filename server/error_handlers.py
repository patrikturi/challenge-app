from server import errors


def handle_bad_request(e):
    return {'success': False, 'message': f'Error: "{e}"'}


def register(app):
    app.register_error_handler(errors.UserError, handle_bad_request)
