"""add bubbles chat and what changed feature columns

Revision ID: 002
Revises: 001
Create Date: 2026-02-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Get connection and check existing columns
    conn = op.get_bind()
    inspector = inspect(conn)
    
    # Add columns to supportconversation table
    try:
        existing_columns = [col['name'] for col in inspector.get_columns('supportconversation')]
        with op.batch_alter_table('supportconversation') as batch_op:
            if 'was_helpful' not in existing_columns:
                batch_op.add_column(sa.Column('was_helpful', sa.Boolean(), nullable=True, server_default='0'))
            if 'resolution_type' not in existing_columns:
                batch_op.add_column(sa.Column('resolution_type', sa.String(), nullable=True))
    except Exception as e:
        print(f"Note: supportconversation table migration skipped or already done: {e}")
    
    # Add columns to user table for "What Changed" feature
    try:
        existing_columns = [col['name'] for col in inspector.get_columns('user')]
        with op.batch_alter_table('user') as batch_op:
            if 'last_seen_at' not in existing_columns:
                batch_op.add_column(sa.Column('last_seen_at', sa.DateTime(), nullable=True))
            if 'away_summary_preference' not in existing_columns:
                batch_op.add_column(sa.Column('away_summary_preference', sa.String(), nullable=True, server_default='ask'))
    except Exception as e:
        print(f"Note: user table migration skipped or already done: {e}")


def downgrade():
    # Remove columns from supportconversation table
    with op.batch_alter_table('supportconversation') as batch_op:
        batch_op.drop_column('resolution_type')
        batch_op.drop_column('was_helpful')
    
    # Remove columns from user table
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('away_summary_preference')
        batch_op.drop_column('last_seen_at')
