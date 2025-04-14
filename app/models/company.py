from tortoise.models import Model
from tortoise import fields

class Company(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    legal_name = fields.CharField(max_length=255, null=True)
    tax_id = fields.CharField(max_length=100, null=True)
    email = fields.CharField(max_length=255, null=True)
    phone = fields.CharField(max_length=20, null=True)
    website = fields.CharField(max_length=255, null=True)
    address = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Location(Model):
    id = fields.IntField(pk=True)
    company = fields.ForeignKeyField("models.Company", related_name="locations", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)
    code = fields.CharField(max_length=50, unique=True)
    location_type = fields.CharField(max_length=50, default="branch")
    country = fields.CharField(max_length=100)
    city = fields.CharField(max_length=100)
    address = fields.TextField()

    def __str__(self):
        return f"{self.name} - {self.company.name}"

class Department(Model):
    id = fields.IntField(pk=True)
    company = fields.ForeignKeyField("models.Company", related_name="departments", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=100)
    description = fields.TextField()
    manager_id = fields.IntField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ({self.company.name})"

class Invitation(Model):
    id = fields.IntField(pk=True)
    invitation_id = fields.CharField(max_length=12, unique=True)
    company = fields.ForeignKeyField("models.Company", related_name="invitations", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)
    role = fields.CharField(max_length=30)
    department = fields.ForeignKeyField("models.Department", related_name="invitations", null=True, on_delete=fields.SET_NULL)
    status = fields.CharField(max_length=10, default="pending")

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.status}"
