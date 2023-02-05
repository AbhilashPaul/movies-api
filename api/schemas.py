from datetime import date

from marshmallow import Schema, fields, ValidationError

from api.constants import CHARACTER_LIMIT_TITLE, CHARACTER_LIMIT_DESCRIPTION


def validate_character_count(data: str, max_length: int):
    if len(data) > max_length:
        raise ValidationError(f"Text input must be less than {max_length} characters.")


def validate_title(data: str):
    validate_character_count(data, CHARACTER_LIMIT_TITLE)


def validate_description(data: str):
    validate_character_count(data, CHARACTER_LIMIT_DESCRIPTION)


def validate_release_year(data: int):
    if data > date.today().year:
        raise ValidationError("Year of release must be less than or equal to current year.")


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate_title)
    description = fields.Str(required=True, validate=validate_description)
    release_year = fields.Int(required=True, validate=validate_release_year)
    duration_minutes = fields.Int(required=True)
    rating = fields.Float(required=True)
    likes = fields.Int(dump_only=True)
    dislikes = fields.Int(dump_only=True)


class MovieLikesSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    likes = fields.Int()


class MovieDislikesSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    dislikes = fields.Int()
