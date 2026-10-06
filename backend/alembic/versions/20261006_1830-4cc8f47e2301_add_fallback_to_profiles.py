"""Add Fallback to profiles

Revision ID: 4cc8f47e2301
Revises: 65e07a32e5d9
Create Date: 2026-10-06 18:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlmodel.sql.sqltypes
from app_logger import ModuleLogger


# revision identifiers, used by Alembic.
revision: str = '4cc8f47e2301'
down_revision: Union[str, None] = '65e07a32e5d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

logger = ModuleLogger("AlembicMigrations")


def upgrade() -> None:
    op.execute("PRAGMA foreign_keys=OFF")

    # Off by default: every matching profile downloads its own trailer, as
    # before this setting existed.
    with op.batch_alter_table("trailerprofile", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "fallback",
                sa.Boolean(),
                server_default="0",
                nullable=False,
            )
        )

    op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    op.execute("PRAGMA foreign_keys=OFF")

    with op.batch_alter_table("trailerprofile", schema=None) as batch_op:
        batch_op.drop_column("fallback")

    op.execute("PRAGMA foreign_keys=ON")
