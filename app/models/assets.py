from tortoise.models import Model
from tortoise import fields
from tortoise.fields import JSONField
import random
from datetime import date


# ✅ Asset Categories
class AssetCategory(str):
    VEHICLE = "vehicle"
    IT_EQUIPMENT = "it_equipment"
    FURNITURE = "furniture"
    OFFICE_EQUIPMENT = "office_equipment"
    MANUFACTURING_EQUIPMENT = "manufacturing_equipment"

# ✅ Asset Status Choices
class AssetStatus(str):
    IN_SERVICE = "in_service"
    UNDER_REPAIR = "under_repair"
    IN_TRANSIT = "in_transit"
    DISPOSED = "disposed"

# ✅ Asset Model
class Asset(Model):
    id = fields.IntField(pk=True)
    asset_id = fields.CharField(max_length=12, unique=True)
    company = fields.ForeignKeyField("models.Company", related_name="assets", on_delete=fields.CASCADE)
    location = fields.ForeignKeyField("models.Location", related_name="assets", null=True, on_delete=fields.SET_NULL)
    name = fields.CharField(max_length=255)
    category = fields.CharField(max_length=50)
    department = fields.CharField(max_length=100)
    assigned = fields.CharField(max_length=100)
    asset_details = JSONField(null=True)
    purchase_price = fields.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = fields.DateField()
    status = fields.CharField(max_length=20, default=AssetStatus.IN_SERVICE)
    
    async def generate_asset_id(self):
        """Generate a unique asset ID (e.g., AST-1001)."""
        while True:
            random_number = random.randint(1000, 9999)
            asset_id = f"AST-{random_number}"
            exists = await Asset.filter(asset_id=asset_id).exists()
            if not exists:
                return asset_id

    async def save(self, *args, **kwargs):
        """Auto-generate asset_id on first save."""
        if not self.asset_id:
            self.asset_id = await self.generate_asset_id()
        await super().save(*args, **kwargs)

# ✅ Vendor Model
class Vendor(Model):
    id = fields.IntField(pk=True)
    vendor_id = fields.CharField(max_length=12, unique=True)
    company = fields.ForeignKeyField("models.Company", related_name="vendors", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=20)
    address = fields.TextField(null=True)
    service_categories = fields.TextField()
    status = fields.CharField(max_length=20, default="active")

    async def generate_vendor_id(self):
        """Generate a unique vendor ID (e.g., VEN-1001)."""
        while True:
            random_number = random.randint(1000, 9999)
            vendor_id = f"VEN-{random_number}"
            exists = await Vendor.filter(vendor_id=vendor_id).exists()
            if not exists:
                return vendor_id

    async def save(self, *args, **kwargs):
        """Auto-generate vendor_id on first save."""
        if not self.vendor_id:
            self.vendor_id = await self.generate_vendor_id()
        await super().save(*args, **kwargs)

# ✅ Maintenance Model
class Maintenance(Model):
    id = fields.IntField(pk=True)
    task_id = fields.CharField(max_length=12, unique=True)
    asset = fields.ForeignKeyField("models.Asset", related_name="maintenances", on_delete=fields.CASCADE)
    company = fields.ForeignKeyField("models.Company", related_name="maintenances", on_delete=fields.CASCADE)
    maintenance_type = fields.CharField(max_length=30)
    description = fields.TextField()
    scheduled_date = fields.DateField()
    cost = fields.DecimalField(max_digits=10, decimal_places=2)
    vendor = fields.ForeignKeyField("models.Vendor", related_name="maintenances", null=True, on_delete=fields.SET_NULL)
    status = fields.CharField(max_length=20, default="scheduled")

    async def generate_task_id(self):
        """Generate a unique maintenance task ID (e.g., MAIN-1001)."""
        while True:
            random_number = random.randint(1000, 9999)
            task_id = f"MAIN-{random_number}"
            exists = await Maintenance.filter(task_id=task_id).exists()
            if not exists:
                return task_id

    async def save(self, *args, **kwargs):
        """Auto-generate task_id and update status based on scheduled date."""
        if not self.task_id:
            self.task_id = await self.generate_task_id()

        # Auto-update status
        today = date.today()
        if self.status == "scheduled":
            if self.scheduled_date == today:
                self.status = "in_progress"
            elif self.scheduled_date < today:
                self.status = "incomplete"

        await super().save(*args, **kwargs)

# ✅ AssetTransfer Model
class AssetTransfer(Model):
    id = fields.IntField(pk=True)
    company = fields.ForeignKeyField("models.Company", related_name="asset_transfers", on_delete=fields.CASCADE)
    asset = fields.ForeignKeyField("models.Asset", related_name="transfers")
    from_location = fields.ForeignKeyField("models.Location", related_name="assets_from", null=True, on_delete=fields.SET_NULL)
    from_department = fields.CharField(max_length=100)
    from_assigned = fields.CharField(max_length=100)
    to_location = fields.ForeignKeyField("models.Location", related_name="assets_to", null=True, on_delete=fields.SET_NULL)
    to_department = fields.CharField(max_length=100)
    to_assigned = fields.CharField(max_length=100)
    transferred_by = fields.CharField(max_length=100)
    transfer_date = fields.DateField()
    note = fields.TextField(max_length=400)

# ✅ AssetDisposal Model
class AssetDisposal(Model):
    id = fields.IntField(pk=True)
    asset = fields.ForeignKeyField("models.Asset", related_name="disposals", on_delete=fields.CASCADE)
    company = fields.ForeignKeyField("models.Company", related_name="disposals")
    method = fields.CharField(max_length=50)  # sale, scrap, donation
    disposal_date = fields.DateField()
    value_received = fields.DecimalField(max_digits=10, decimal_places=2)
    note = fields.TextField(null=True)
    approved_by = fields.CharField(max_length=100)
