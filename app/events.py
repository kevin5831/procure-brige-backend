from tortoise.signals import post_save
from app.models.user import User
from app.models.company import Company, Department, Invitation
from app.models.company import Company

@post_save(User)
async def create_user_company(sender, instance: User, created: bool, **kwargs):
    """Automatically create a company for a new user."""
    if created and not instance.company:
        company = await Company.create(
            name=f"{instance.first_name}'s Organization",
            email=instance.email
        )
        instance.company = company
        await instance.save()


@post_save(Invitation)
async def handle_invitation(sender, instance: Invitation, created: bool, **kwargs):
    """Check if the invited user exists and assign them to the company & role"""
    if created:
        user = await User.get_or_none(email=instance.email)
        if user:
            user.company = instance.company
            user.role = instance.role
            user.department = instance.department
            await user.save()
            instance.status = "active"
            await instance.save()


@post_save(Company)
async def create_departments(sender, instance: Company, created: bool, **kwargs):
    """Automatically create default departments when a new company is added"""
    if created:
        departments = [
            {"name": "IT", "description": "Information Technology Department"},
            {"name": "Finance", "description": "Financial Operations Department"},
            {"name": "Human Resources", "description": "Human Resources Department"},
            {"name": "Operations", "description": "Operations Department"},
        ]
        for dept in departments:
            await Department.create(company=instance, name=dept["name"], description=dept["description"])
