from datetime import datetime
from ariadne import convert_kwargs_to_snake_case
from api import db
from api.models import Post

@convert_kwargs_to_snake_case
def create_post_resolver(obj, info, title, description, created_at=None):
    try:
        today = datetime.today()
        post = Post(
            title=title,
            description=description,
            created_at=created_at if created_at else today.strftime('%b-%d-%Y')
        )
        db.session.add(post)
        db.session.commit()
        payload = {
            'success': True,
            'post': post.to_dict()
        }
    except ValueError:
        payload = {
            'success': False,
            'errors': ['Incorrect date format provided. Date should be in the format dd-mm-yyyy format']
        }
    return payload


@convert_kwargs_to_snake_case
def update_post_resolver(obj, info, id, title, description):
    try:
        post = Post.query.get(id)
        if post:
            post.title = title
            post.description = description
        db.session.add(post)
        db.session.commit()
        payload = {
            'success': True,
            'post': post.to_dict()
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': [f'Item matching id {id} not found']
        }
    return payload


@convert_kwargs_to_snake_case
def delete_post_resolver(obj, info, id):
    try:
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        payload = {
            'success': True,
            'post': post.to_dict()
        }
    except AttributeError:
        payload = {
            'success': False,
            'errors': ['Not found']
        }
    return payload