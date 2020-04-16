from flask import Blueprint

from app.api.v1.views import Submit, Status

blueprint = Blueprint("v1", __name__)

blueprint.add_url_rule('/submit', view_func=Submit.as_view('submit'))
blueprint.add_url_rule('/status/<job_id>', view_func=Status.as_view('status'))
