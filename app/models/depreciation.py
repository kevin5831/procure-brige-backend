from tortoise.models import Model
from tortoise.signals import pre_save
from tortoise import fields

# ✅ Depreciation Model
class Depreciation(Model):    
    category = fields.CharField(max_length=50, pk=True)
    residual_value = fields.IntField()
    useful_life_ifrs = fields.IntField()
    useful_life_tax = fields.IntField()
    
    def __str__(self):
        return self.name