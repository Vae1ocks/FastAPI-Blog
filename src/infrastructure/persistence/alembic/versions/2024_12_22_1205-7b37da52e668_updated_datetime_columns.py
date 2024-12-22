"""Updated datetime columns

Revision ID: 7b37da52e668
Revises: c2c73c06bb90
Create Date: 2024-12-22 12:05:29.393082

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7b37da52e668"
down_revision: Union[str, None] = "c2c73c06bb90"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "articles",
        "created_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
        existing_server_default=sa.text("(now() AT TIME ZONE 'utc'::text)"),
    )
    op.alter_column(
        "articles",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.TIMESTAMP(timezone=True),
        existing_nullable=True,
    )
    op.create_unique_constraint(op.f("uq_articles_id"), "articles", ["id"])
    op.create_unique_constraint(op.f("uq_comments_id"), "comments", ["id"])
    op.create_unique_constraint(op.f("uq_users_id"), "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("uq_users_id"), "users", type_="unique")
    op.drop_constraint(op.f("uq_comments_id"), "comments", type_="unique")
    op.drop_constraint(op.f("uq_articles_id"), "articles", type_="unique")
    op.alter_column(
        "articles",
        "updated_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
    )
    op.alter_column(
        "articles",
        "created_at",
        existing_type=sa.TIMESTAMP(timezone=True),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        existing_server_default=sa.text("(now() AT TIME ZONE 'utc'::text)"),
    )
    # ### end Alembic commands ###
