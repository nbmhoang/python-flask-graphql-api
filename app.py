from api import app
from api import db
from api import models

from ariadne import load_schema_from_path
from ariadne import make_executable_schema
from ariadne import graphql_sync
from ariadne import snake_case_fallback_resolvers
from ariadne import QueryType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import request
from flask import jsonify
from api.mutations import create_post_resolver
from api.mutations import delete_post_resolver
from api.mutations import update_post_resolver

from api.queries import getPost_resolver
from api.queries import listPosts_resolver

query = QueryType()
query.set_field('listPosts', listPosts_resolver)
query.set_field('getPost', getPost_resolver)

mutation = MutationType()
mutation.set_field('createPost', create_post_resolver)
mutation.set_field('updatePost', update_post_resolver)
mutation.set_field("deletePost", delete_post_resolver)

type_defs = load_schema_from_path('schema.graphql')
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

@app.route('/graphql', methods=['GET'])
def graphql_playground():
    return PLAYGROUND_HTML

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code