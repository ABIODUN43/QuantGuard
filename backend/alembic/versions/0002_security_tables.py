"""security tables

Revision ID: 0002_security_tables
Revises: 0001_initial_schema
Create Date: 2026-05-20
"""

revision = "0002_security_tables"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Security tables were folded into 0001 before the production Blueprint deploy.
    # Keep this revision as a no-op so databases already stamped at 0001 can advance.
    pass


def downgrade() -> None:
    pass
