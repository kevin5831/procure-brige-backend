from tortoise.models import Model
from tortoise import fields


# User Types
class UserType(str):
    ADMIN = "admin"
    STAFF = "staff"

# Roles
class Role(str):
    ACCOUNTANT = "accountant"
    FINANCE_MANAGER = "finance_manager"
    MAINTENANCE_MANAGER = "maintenance_manager"
    TECHNICIAN = "technician"
    AUDITOR = "auditor"
    ASSET_MANAGER = "asset_manager"
    DEPARTMENT_MANAGER = "department_manager"

# Permission Types
class PermissionType(str):
    CREATE_ASSETS = "create_assets"
    VIEW_ASSETS = "view_assets"
    EDIT_ASSETS = "edit_assets"
    DELETE_ASSETS = "delete_assets"
    
    CREATE_REQUESTS = "create_requests"
    APPROVE_REQUESTS = "approve_requests"
    VIEW_REQUESTS = "view_requests"

    VIEW_FINANCIAL_DATA = "view_financial_data"
    EDIT_FINANCIAL_RECORDS = "edit_financial_records"
    APPROVE_TRANSACTIONS = "approve_transactions"

# Permissions Model
class Permission(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, unique=True)
    codename = fields.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# User Model
class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=100, null=True)
    password = fields.CharField(max_length=255)
    user_type = fields.CharField(max_length=10, default=UserType.ADMIN)
    role = fields.CharField(max_length=30, null=True, blank=True)
    is_staff = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    company = fields.ForeignKeyField("models.Company", related_name="users", null=True)
    department_id = fields.IntField(null=True)
    permissions = fields.ManyToManyField("models.Permission", related_name="users")

    def __str__(self):
        return self.email
