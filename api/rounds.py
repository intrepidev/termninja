from sanic import Blueprint
from sanic.response import json, text
from sanic.exceptions import abort
from termninja import db


bp = Blueprint('round_views', url_prefix='/round')


def validate_page(request_page):
    try:
        page = int(request_page)
        if page < 0:
            page = 0
        return page
    except ValueError:
        abort(400, 'invalid page')


@bp.route('/', methods=['GET'])
async def list_rounds(request):
    request_page = request.args.get('page', '0')
    page = validate_page(request_page)
    results = await db.rounds.list_rounds_played(page=page)
    return json(results)


@bp.route('/<round_id:int>', methods=['GET'])
async def get_round_details(request, round_id):
    result = await db.rounds.get_round_details(round_id)
    if result is None:
        abort(404)
    return json(result)
