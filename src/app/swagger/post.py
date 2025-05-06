from flask_restx import fields

from app.extensions import api

post_input_sw_model = api.model(
    'PostInput',
    {
        'title': fields.String(required=True),
        'body': fields.String(required=True),
        'user_id': fields.Integer(required=True, min=1),
    },
)

post_patch_input_sw_model = api.model(
    'PostPatchInput',
    {
        'title': fields.String(),
        'body': fields.String(),
        'user_id': fields.Integer(min=1),
    },
)

post_sw_model = api.model(
    'Post',
    {
        'id': fields.Integer(required=True),
        'title': fields.String,
        'body': fields.String,
        'user_id': fields.Integer(min=1),
    },
)
