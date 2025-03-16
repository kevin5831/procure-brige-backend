from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "company" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "legal_name" VARCHAR(255),
    "tax_id" VARCHAR(100),
    "email" VARCHAR(255),
    "phone" VARCHAR(20),
    "website" VARCHAR(255),
    "address" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "vendor" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "vendor_id" VARCHAR(12) NOT NULL UNIQUE,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "phone" VARCHAR(20) NOT NULL,
    "address" TEXT,
    "service_categories" TEXT NOT NULL,
    "status" VARCHAR(20) NOT NULL DEFAULT 'active',
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "department" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT NOT NULL,
    "manager_id" INT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "invitation" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "invitation_id" VARCHAR(12) NOT NULL UNIQUE,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "role" VARCHAR(30) NOT NULL,
    "status" VARCHAR(10) NOT NULL DEFAULT 'pending',
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE,
    "department_id" INT REFERENCES "department" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "location" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "code" VARCHAR(50) NOT NULL UNIQUE,
    "location_type" VARCHAR(50) NOT NULL DEFAULT 'branch',
    "country" VARCHAR(100) NOT NULL,
    "city" VARCHAR(100) NOT NULL,
    "address" TEXT NOT NULL,
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "asset" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "asset_id" VARCHAR(12) NOT NULL UNIQUE,
    "name" VARCHAR(255) NOT NULL,
    "category" VARCHAR(50) NOT NULL,
    "purchase_price" DECIMAL(12,2) NOT NULL,
    "purchase_date" DATE NOT NULL,
    "status" VARCHAR(20) NOT NULL DEFAULT 'in_service',
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE,
    "location_id" INT REFERENCES "location" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "maintenance" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "task_id" VARCHAR(12) NOT NULL UNIQUE,
    "maintenance_type" VARCHAR(30) NOT NULL,
    "description" TEXT NOT NULL,
    "scheduled_date" DATE NOT NULL,
    "cost" DECIMAL(10,2) NOT NULL,
    "status" VARCHAR(20) NOT NULL DEFAULT 'scheduled',
    "asset_id" INT NOT NULL REFERENCES "asset" ("id") ON DELETE CASCADE,
    "company_id" INT NOT NULL REFERENCES "company" ("id") ON DELETE CASCADE,
    "vendor_id" INT REFERENCES "vendor" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "depreciation" (
    "category" VARCHAR(50) NOT NULL PRIMARY KEY,
    "residual_value" INT NOT NULL,
    "useful_life_ifrs" INT NOT NULL,
    "useful_life_tax" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "permission" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "codename" VARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "first_name" VARCHAR(100),
    "last_name" VARCHAR(100),
    "password" VARCHAR(255) NOT NULL,
    "user_type" VARCHAR(10) NOT NULL DEFAULT 'admin',
    "role" VARCHAR(30),
    "is_staff" BOOL NOT NULL DEFAULT False,
    "is_active" BOOL NOT NULL DEFAULT True,
    "department_id" INT,
    "company_id" INT REFERENCES "company" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_permission" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "permission_id" INT NOT NULL REFERENCES "permission" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_user_permis_user_id_944080" ON "user_permission" ("user_id", "permission_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
