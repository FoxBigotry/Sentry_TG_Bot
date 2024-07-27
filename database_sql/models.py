from tortoise import fields, models


class SQLErrorModel(models.Model):
    id = fields.IntField(pk=True)
    error_id = fields.BigIntField()
    project_name = fields.CharField(max_length=255)
    type_error = fields.CharField(max_length=255)
    value_error = fields.CharField(max_length=255)
    url_error = fields.CharField(max_length=255)
    event_id = fields.CharField(max_length=255)
    datetime = fields.DatetimeField(max_length=255)
    topic_id = fields.IntField()
