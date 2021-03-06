from api import Resource, abort, reqparse, auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields

@doc(description='Api for notes.',tags=['Users'])
class UserResource(MethodResource):
    @doc(summary="Get User by id")
    @marshal_with(UserSchema, code=200)
    @doc(responses= {"404": {"description": "User not found"}})
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200

    @auth.login_required(role="admin")
    # @auth.login_required
    @doc(security=[{"basicAuth": []}])
    @doc(summary="Edit User by id")
    @marshal_with(UserSchema, code=200)
    @use_kwargs({"username": fields.Str(required=True)})
    def put(self, user_id,**kwargs):
        user = UserModel.query.get(user_id)
        user.username = kwargs["username"]
        user.save()
        return user, 200

    @auth.login_required
    def delete(self, user_id):
        raise NotImplemented  # не реализовано!

@doc(tags=['Users'])
class UsersListResource(MethodResource):
    @doc(summary="Get a List of Users")
    @marshal_with(UserSchema(many=True), code=200)
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @doc(summary="Creat New User")
    @marshal_with(UserSchema, code=201)
    @use_kwargs(UserRequestSchema, location=('json'))
    def post(self,**kwargs):
        # parser = reqparse.RequestParser()
        # parser.add_argument("username", required=True)
        # parser.add_argument("password", required=True)
        # user_data = parser.parse_args()
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        return user, 201
