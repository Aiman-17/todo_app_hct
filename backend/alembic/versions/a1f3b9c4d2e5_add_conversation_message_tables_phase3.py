"""Add conversation and message tables for Phase III AI chatbot

Revision ID: a1f3b9c4d2e5
Revises: 57b259b29a5e
Create Date: 2026-01-14 17:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1f3b9c4d2e5'
down_revision: Union[str, None] = '57b259b29a5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Phase III: Create conversations table ###
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for conversations table
    op.create_index('ix_conversations_user_created', 'conversations', ['user_id', 'created_at'], unique=False)
    op.create_index('idx_active_conversations', 'conversations', ['user_id'], unique=False,
                    postgresql_where=sa.text('deleted_at IS NULL'))

    # ### Phase III: Create messages table ###
    op.create_table(
        'messages',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes for messages table
    op.create_index('ix_messages_conversation_created', 'messages', ['conversation_id', 'created_at'], unique=False)
    op.create_index('idx_active_messages', 'messages', ['conversation_id'], unique=False,
                    postgresql_where=sa.text('deleted_at IS NULL'))
    # ### end Phase III commands ###


def downgrade() -> None:
    # ### Phase III: Drop tables in reverse order ###
    # Drop messages table first (has FK to conversations)
    op.drop_index('idx_active_messages', table_name='messages')
    op.drop_index('ix_messages_conversation_created', table_name='messages')
    op.drop_table('messages')

    # Drop conversations table
    op.drop_index('idx_active_conversations', table_name='conversations')
    op.drop_index('ix_conversations_user_created', table_name='conversations')
    op.drop_table('conversations')
    # ### end Phase III commands ###
