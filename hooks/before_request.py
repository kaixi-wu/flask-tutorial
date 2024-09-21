from flask import g, request, session


def register_before_hooks(app) -> None:
    @app.before_request
    def load_user_merchant_id():
        user_id = session.get("user_id")

        if user_id is None:
            g.user_id = None
        else:
            g.user_id = user_id
