"""empty message

Revision ID: df9b61c75170
Revises: 9da0012a44c6
Create Date: 2024-04-29 18:43:05.550163

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'df9b61c75170'
down_revision: Union[str, None] = '9da0012a44c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('migration')
    op.create_unique_constraint(None, 'credential_offer', ['id'])
    op.create_unique_constraint(None, 'credential_revocation_status_list', ['id'])
    op.create_unique_constraint(None, 'data_agreement', ['id'])
    op.add_column('issue_credential_record', sa.Column('limitedDisclosure', sa.Boolean(), server_default='True', nullable=False))
    op.create_unique_constraint(None, 'issue_credential_record', ['id'])
    op.create_unique_constraint(None, 'organisation', ['id'])
    op.create_unique_constraint(None, 'v2_data_agreement', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'v2_data_agreement', type_='unique')
    op.drop_constraint(None, 'organisation', type_='unique')
    op.drop_constraint(None, 'issue_credential_record', type_='unique')
    op.drop_column('issue_credential_record', 'limitedDisclosure')
    op.drop_constraint(None, 'data_agreement', type_='unique')
    op.drop_constraint(None, 'credential_revocation_status_list', type_='unique')
    op.drop_constraint(None, 'credential_offer', type_='unique')
    op.create_table('migration',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('isApplied', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('createdAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updatedAt', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='migration_pkey'),
    sa.UniqueConstraint('name', name='migration_name_key')
    )
    # ### end Alembic commands ###
