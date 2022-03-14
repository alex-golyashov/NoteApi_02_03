from api import Resource, abort, reqparse, auth
from api.models.tag import TagModel
from api.schemas.tag import tag_schema, tags_schema, TagSchema, TagRequestSchema
from api.schemas.note import NoteSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from webargs import fields
from api.models.note import NoteModel

@doc(description='Api for tags.',tags=['Tags'])
class TagResource(MethodResource):
    @marshal_with(TagSchema, code=200)
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag is None:
            abort(404, error=f"Tag with id={tag_id} not found")
        return tag, 200


@doc(tags=['Tags'])
class TagsListResource(MethodResource):
    @use_kwargs(TagRequestSchema, location=('json'))
    @marshal_with(TagSchema, code=201)
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        if tag.id is None:
            abort(400, error=f"Tag with name:{tag.name} already exist")
        return tag, 201

from webargs import fields

# PUT: /notes/<note_id>/tags
@doc(tags=['Notes'])
class NoteSetTagsResource(MethodResource):
   @doc(summary="Set tags to Note")
   @use_kwargs({"tags": fields.List(fields.Int())}, location=('json'))
   @marshal_with(NoteSchema)
   def put(self, note_id, **kwargs):
       note = NoteModel.query.get(note_id)
       if not note:
           abort(404, error=f"note {note_id} not found")
       print("note kwargs = ", kwargs)
       for tag_id in kwargs["tags"]:
           tag = TagModel.query.get(tag_id)
           #TODO:  добавить проверку существования тега
           # FIXME:
           note.tags.append(tag)

       return note, 200

