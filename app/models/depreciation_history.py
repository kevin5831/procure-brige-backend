from tortoise.models import Model
from tortoise.signals import pre_save
from tortoise import fields
from datetime import date

# ✅ Depreciation Model
class DepreciationHistory(Model):    
    id = fields.IntField(pk=True)
    asset_id = fields.ForeignKeyField("models.Asset", related_name="history", on_delete=fields.CASCADE)
    depreciation = fields.JSONField()
    update_date = fields.DateField()
    
    def __str__(self):
        return self.name