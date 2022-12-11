import os

from flask import Flask, request, jsonify
from marshmallow import ValidationError


from builder import query_builder
from models import BatchRequestParams

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=['POST'])
def perform_query():
    try:
        params = BatchRequestParams().load(data=request.json)
    except ValidationError as error:
        return jsonify(error.messages), 400

    result = None
    for query in params['queries']:
        result = query_builder(
            cmd=query['cmd'],
            value=query['value'],
            data=result,
        )

    return jsonify(result)

    # # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # # вернуть пользователю сформированный результат



app.run()
