"""
Phase III: Model Context Protocol (MCP) tool implementations.

This package provides MCP tools that expose Phase II task operations
to AI agents. All tools enforce user isolation and operate through
the existing Phase II service layer (READ-ONLY imports).

Available MCP Tools:
- add_task: Create new task
- list_tasks: Retrieve tasks with filtering
- complete_task: Toggle task completion status
- delete_task: Soft delete a task
- update_task: Modify task fields
"""
