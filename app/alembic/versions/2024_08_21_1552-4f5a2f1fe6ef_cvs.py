"""cvs

Revision ID: 4f5a2f1fe6ef
Revises: 89a517f53997
Create Date: 2024-08-21 15:52:14.681798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f5a2f1fe6ef'
down_revision: Union[str, None] = '89a517f53997'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cvs',
    sa.Column('github_profile_link', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('full_path', sa.String(), nullable=False),
    sa.Column('json_data', sa.JSON(), nullable=False),
    sa.Column('user_uuid', sa.UUID(), nullable=False),
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['users.uuid'], name=op.f('fk_cvs_user_uuid_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_cvs')),
    sa.UniqueConstraint('uuid', name=op.f('uq_cvs_uuid'))
    )
    op.create_index(op.f('ix_cvs_github_profile_link'), 'cvs', ['github_profile_link'], unique=False)
    op.create_unique_constraint(op.f('uq_users_uuid'), 'users', ['uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_users_uuid'), 'users', type_='unique')
    op.drop_index(op.f('ix_cvs_github_profile_link'), table_name='cvs')
    op.drop_table('cvs')
    # ### end Alembic commands ###
