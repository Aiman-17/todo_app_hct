# Data Model: Phase III – Todo AI Chatbot

**Phase**: Phase III - AI Conversational Layer
**Date**: 2026-01-13
**Purpose**: Database schema design for conversation persistence

## Overview

Phase III extends the existing database schema with two new tables to support conversational AI:
- **Conversation**: Groups related messages between user and AI assistant
- **Message**: Individual chat messages (append-only for audit trail)

The existing **Task** model from Phase I/II remains unchanged (additive-only principle).

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │ (Existing - Phase II)
│ (Phase II)  │
└──────┬──────┘
       │ 1
       │
       │ N
┌──────┴───────────┐         ┌─────────────┐
│  Conversation    │         │    Task     │ (Existing - Phase I)
│  (Phase III)     │         │ (Phase I/II)│
└──────┬───────────┘         └─────────────┘
       │ 1                          │
       │                            │
       │ N                          │
┌──────┴───────────┐                │
│    Message       │                │
│  (Phase III)     │                │
└──────────────────┘                │
       │                            │
       └────────────────────────────┘
         (Both reference user_id)
```

## Entities

### 1. Conversation (NEW)

**Purpose**: Represents a chat thread between a user and the AI assistant.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique conversation identifier |
| user_id | UUID | NOT NULL, FOREIGN KEY → users(id) ON DELETE CASCADE | Owner of the conversation |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Conversation creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Last message timestamp |
| deleted_at | TIMESTAMP WITH TIME ZONE | NULLABLE | Soft delete timestamp (NULL if active) |

**Indexes**:
- `PRIMARY KEY (id)` - Fast lookup by conversation ID
- `INDEX idx_user_conversations (user_id, created_at DESC)` - List user's conversations

**Relationships**:
- **One-to-Many**: User → Conversation (one user has many conversations)
- **One-to-Many**: Conversation → Message (one conversation has many messages)

**Validation Rules**:
- `user_id` must reference existing user
- `created_at` cannot be in the future
- `updated_at` >= `created_at`

**State Transitions**:
- **Created**: On first message from user
- **Updated**: On every new message (trigger updates `updated_at`)
- **Soft Deleted**: Set `deleted_at` timestamp (per clarification 2026-01-14)
- **Archived**: Optional asynchronous job MAY copy to `archived_conversations` table

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "created_at": "2026-01-13T10:30:00Z",
  "updated_at": "2026-01-13T10:35:00Z"
}
```

### 2. Message (NEW)

**Purpose**: Individual chat message within a conversation (append-only).

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | BIGSERIAL | PRIMARY KEY | Auto-incrementing message ID |
| conversation_id | UUID | NOT NULL, FOREIGN KEY → conversations(id) ON DELETE CASCADE | Parent conversation |
| user_id | UUID | NOT NULL, FOREIGN KEY → users(id) ON DELETE CASCADE | Message owner (for isolation) |
| role | VARCHAR(20) | NOT NULL, CHECK (role IN ('user', 'assistant')) | Message sender role |
| content | TEXT | NOT NULL | Message text content |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Message creation timestamp |
| deleted_at | TIMESTAMP WITH TIME ZONE | NULLABLE | Soft delete timestamp (NULL if active) |

**Indexes**:
- `PRIMARY KEY (id)` - Fast lookup by message ID
- `INDEX idx_conversation_messages (conversation_id, created_at ASC)` - List messages in conversation order

**Relationships**:
- **Many-to-One**: Message → Conversation (many messages belong to one conversation)
- **Many-to-One**: Message → User (many messages belong to one user)

**Validation Rules**:
- `role` must be either 'user' or 'assistant'
- `content` cannot be empty string
- `content` max length: 10,000 characters
- `user_id` must match conversation's `user_id` (enforced in application layer)

**State Transitions**:
- **Created**: On message send (user) or agent response (assistant)
- **NEVER UPDATED OR DELETED**: Append-only for audit trail

**Example**:
```json
{
  "id": 1,
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "role": "user",
  "content": "Add a task to buy groceries",
  "created_at": "2026-01-13T10:30:00Z"
},
{
  "id": 2,
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "role": "assistant",
  "content": "✓ Created task: 'Buy groceries' (ID: 42). I've added it to your list!",
  "created_at": "2026-01-13T10:30:02Z"
}
```

### 3. Task (EXISTING - Phase I/II)

**Purpose**: Todo item managed by users (referenced but not modified in Phase III).

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT | Task ID |
| user_id | UUID | NOT NULL, FOREIGN KEY → users(id) | Task owner |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULLABLE | Optional description |
| completed | BOOLEAN | DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Creation timestamp |
| updated_at | TIMESTAMP WITH TIME ZONE | DEFAULT NOW() | Last update timestamp |

**Phase III Interaction**:
- MCP tools (add_task, list_tasks, complete_task, delete_task, update_task) operate on this table
- No schema changes in Phase III
- All operations scoped by user_id (user isolation)

## SQL Schema

```sql
-- Phase III: Conversation Table
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
);

CREATE INDEX idx_user_conversations ON conversations(user_id, created_at DESC);
CREATE INDEX idx_active_conversations ON conversations(user_id) WHERE deleted_at IS NULL;

-- Phase III: Message Table
CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
  content TEXT NOT NULL CHECK (length(content) > 0 AND length(content) <= 10000),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL
);

CREATE INDEX idx_conversation_messages ON messages(conversation_id, created_at ASC);
CREATE INDEX idx_active_messages ON messages(conversation_id) WHERE deleted_at IS NULL;

-- Trigger: Update conversation.updated_at on new message
CREATE OR REPLACE FUNCTION update_conversation_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE conversations
  SET updated_at = NEW.created_at
  WHERE id = NEW.conversation_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_conversation_timestamp
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION update_conversation_timestamp();
```

## SQLModel Python Models

```python
# src/models/conversation.py
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    role: str = Field(nullable=False, max_length=20)  # 'user' or 'assistant'
    content: str = Field(nullable=False, max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(default=None)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    # Validation
    @property
    def is_valid_role(self) -> bool:
        return self.role in ["user", "assistant"]
```

## Migration Script

```python
# backend/alembic/versions/003_add_conversation_tables.py
"""Add conversation and message tables for Phase III

Revision ID: 003_phase3_conversations
Revises: 002_phase2_auth
Create Date: 2026-01-13 10:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '003_phase3_conversations'
down_revision = '002_phase2_auth'
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True)
    )
    op.create_index('idx_user_conversations', 'conversations', ['user_id', 'created_at'], postgresql_ops={'created_at': 'DESC'})
    op.create_index('idx_active_conversations', 'conversations', ['user_id'], postgresql_where=sa.text('deleted_at IS NULL'))

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('deleted_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role'),
        sa.CheckConstraint("length(content) > 0 AND length(content) <= 10000", name='check_content_length')
    )
    op.create_index('idx_conversation_messages', 'messages', ['conversation_id', 'created_at'])
    op.create_index('idx_active_messages', 'messages', ['conversation_id'], postgresql_where=sa.text('deleted_at IS NULL'))

    # Create trigger for updating conversation.updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_conversation_timestamp()
        RETURNS TRIGGER AS $$
        BEGIN
          UPDATE conversations
          SET updated_at = NEW.created_at
          WHERE id = NEW.conversation_id;
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER trigger_update_conversation_timestamp
        AFTER INSERT ON messages
        FOR EACH ROW
        EXECUTE FUNCTION update_conversation_timestamp();
    """)

def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trigger_update_conversation_timestamp ON messages")
    op.execute("DROP FUNCTION IF EXISTS update_conversation_timestamp()")
    op.drop_index('idx_conversation_messages', table_name='messages')
    op.drop_table('messages')
    op.drop_index('idx_user_conversations', table_name='conversations')
    op.drop_table('conversations')
```

## Data Access Patterns

### 1. Create New Conversation
```python
# Start new conversation on first message
conversation = Conversation(user_id=current_user.id)
session.add(conversation)
session.commit()
```

### 2. Append Message
```python
# Add user message
user_message = Message(
    conversation_id=conversation_id,
    user_id=current_user.id,
    role="user",
    content=user_input
)
session.add(user_message)
session.commit()

# Add assistant response
assistant_message = Message(
    conversation_id=conversation_id,
    user_id=current_user.id,
    role="assistant",
    content=ai_response
)
session.add(assistant_message)
session.commit()
```

### 3. Fetch Conversation History
```python
# Get last 50 messages (lazy loading)
messages = session.query(Message)\
    .filter(Message.conversation_id == conversation_id)\
    .order_by(Message.created_at.asc())\
    .limit(50)\
    .all()
```

### 4. List User Conversations
```python
# Get user's recent conversations (exclude soft-deleted)
conversations = session.query(Conversation)\
    .filter(Conversation.user_id == current_user.id)\
    .filter(Conversation.deleted_at.is_(None))\
    .order_by(Conversation.updated_at.desc())\
    .limit(20)\
    .all()
```

### 5. Soft Delete Conversation (Post-Clarification 2026-01-14)
```python
# Soft delete conversation and all associated messages
conversation = session.query(Conversation).filter(
    Conversation.id == conversation_id,
    Conversation.user_id == current_user.id
).first()

if conversation:
    # Set deleted_at on conversation
    conversation.deleted_at = datetime.utcnow()

    # Set deleted_at on all messages
    session.query(Message).filter(
        Message.conversation_id == conversation_id
    ).update({"deleted_at": datetime.utcnow()})

    session.commit()
```

**Deletion Strategy** (per clarification 2026-01-14):
1. Set `deleted_at` timestamp on the conversation record
2. Set `deleted_at` timestamp on all associated messages
3. Exclude soft-deleted records from all user-facing queries
4. An asynchronous archival job MAY copy soft-deleted conversations and messages to `archived_conversations` and `archived_messages` after a defined retention period
5. Archived data is retained for audit and recovery purposes

## Scalability Considerations

### Current Phase (Phase III)
- **Expected Load**: 100 concurrent users, ~1000 messages/day
- **Storage**: ~10MB/day (10KB avg message size)
- **Query Performance**: <100ms with indexes

### Future Optimizations (Phase IV+)
- **Partitioning**: Partition messages table by created_at (monthly) when >10M rows
- **Archiving**: Move messages >1 year old to cold storage
- **Read Replicas**: Add read replicas for conversation history queries
- **Caching**: Cache recent messages in Redis (if query latency >200ms)

## Security & Compliance

### User Isolation
- All queries filter by `user_id` (enforced in MCP tools)
- Foreign key constraints prevent orphaned records
- Cascade delete ensures cleanup when user deleted

### Audit Trail
- Messages are append-only (no UPDATE/DELETE)
- All message content logged (backend only, not exposed to frontend)
- Conversation timestamps track activity

### Data Retention
- Phase III: Indefinite retention (no auto-delete)
- Phase IV+: Implement retention policy (e.g., delete after 2 years with user consent)

## Testing Data

```sql
-- Test data for development
INSERT INTO conversations (id, user_id, created_at, updated_at) VALUES
('550e8400-e29b-41d4-a716-446655440000', '7c9e6679-7425-40de-944b-e07fc1f90ae7', NOW(), NOW());

INSERT INTO messages (conversation_id, user_id, role, content, created_at) VALUES
('550e8400-e29b-41d4-a716-446655440000', '7c9e6679-7425-40de-944b-e07fc1f90ae7', 'user', 'Add a task to buy groceries', NOW()),
('550e8400-e29b-41d4-a716-446655440000', '7c9e6679-7425-40de-944b-e07fc1f90ae7', 'assistant', '✓ Created task: Buy groceries (ID: 42). I've added it to your list!', NOW() + INTERVAL '2 seconds'),
('550e8400-e29b-41d4-a716-446655440000', '7c9e6679-7425-40de-944b-e07fc1f90ae7', 'user', 'Show me all my tasks', NOW() + INTERVAL '5 seconds'),
('550e8400-e29b-41d4-a716-446655440000', '7c9e6679-7425-40de-944b-e07fc1f90ae7', 'assistant', 'Here are your tasks:\n1. Buy groceries (pending)\n2. Call dentist (pending)', NOW() + INTERVAL '6 seconds');
```

## Data Model Summary

Phase III introduces minimal schema changes (2 tables, 1 trigger) that extend the existing Phase II database without modifying any existing tables. The design prioritizes:
- **Simplicity**: Clear relationships, standard patterns
- **Performance**: Proper indexing, lazy loading
- **Security**: User isolation, audit trail
- **Scalability**: Future-proof for Phase IV/V growth

**Ready for contract generation (Phase 1 continued)**
