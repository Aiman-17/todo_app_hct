"""
Rule-based intent classifier as fallback when Gemini API is unavailable.

Uses pattern matching and keyword detection for fast, reliable classification.
No external API calls - works offline and has no rate limits.
"""
import re
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger("mcp_tools")


class RuleBasedClassifier:
    """
    Fast rule-based intent classifier using pattern matching.

    Fallback for when Gemini API is unavailable or rate-limited.
    """

    def __init__(self):
        """Initialize pattern matchers."""
        self.confidence_threshold = 0.7

    def classify(self, message: str, user_id: str = None, correlation_id: str = None, conversation_history: Optional[List] = None) -> Dict[str, Any]:
        """
        Classify user message using rule-based pattern matching.

        Args:
            message: User's natural language message
            user_id: Optional user ID for logging
            correlation_id: Optional correlation ID for tracing
            conversation_history: Optional conversation history (not used in rule-based)

        Returns:
            dict: {
                "intent": str,
                "confidence": float,
                "entities": dict
            }
        """
        message_lower = message.lower().strip()

        # Intent: list_tasks
        if self._is_list_tasks(message_lower):
            return {
                "intent": "list_tasks",
                "confidence": 0.95,
                "entities": self._extract_list_filters(message_lower)
            }

        # Intent: delete_task (check BEFORE complete_task to catch "delete completed")
        if self._is_delete_task(message_lower):
            return {
                "intent": "delete_task",
                "confidence": 0.9,
                "entities": self._extract_task_reference(message_lower)
            }

        # Intent: complete_task
        if self._is_complete_task(message_lower):
            return {
                "intent": "complete_task",
                "confidence": 0.9,
                "entities": self._extract_task_reference(message_lower)
            }

        # Intent: create_task
        if self._is_create_task(message_lower):
            return {
                "intent": "create_task",
                "confidence": 0.9,
                "entities": self._extract_create_entities(message_lower)
            }

        # Intent: update_task
        if self._is_update_task(message_lower):
            return {
                "intent": "update_task",
                "confidence": 0.85,
                "entities": self._extract_update_entities(message_lower)
            }

        # Intent: unclear
        return {
            "intent": "unclear",
            "confidence": 0.2,
            "entities": {}
        }

    def _is_list_tasks(self, msg: str) -> bool:
        """Check if message is requesting task list."""
        keywords = [
            'show', 'list', 'view', 'display', 'see',
            'what', 'tasks', 'todo', 'todos'
        ]
        # Match phrases like "show tasks", "view my tasks", "what tasks"
        return any(kw in msg for kw in ['show', 'list', 'view', 'display']) and \
               any(kw in msg for kw in ['task', 'todo'])

    def _is_create_task(self, msg: str) -> bool:
        """Check if message is creating a task."""
        # Direct patterns that indicate task creation
        if 'remind me' in msg:
            return True

        create_keywords = ['add', 'create', 'new', 'remind']
        task_keywords = ['task', 'todo', 'reminder']

        # "make new tasks for X" pattern
        if 'make' in msg and any(kw in msg for kw in ['task', 'todo']):
            return True

        return (any(kw in msg for kw in create_keywords) and
                any(kw in msg for kw in task_keywords))

    def _is_complete_task(self, msg: str) -> bool:
        """Check if message is marking task complete."""
        complete_keywords = ['mark', 'complete', 'done', 'finish', 'completed']
        return any(kw in msg for kw in complete_keywords)

    def _is_delete_task(self, msg: str) -> bool:
        """Check if message is deleting a task."""
        delete_keywords = ['delete', 'remove', 'trash', 'cancel']

        # Special case: "delete completed tasks" should be handled differently
        # This is a batch operation, not a single task deletion
        if any(kw in msg for kw in delete_keywords):
            # Check if this is a batch delete of completed tasks
            if ('completed' in msg or 'done' in msg or 'finished' in msg) and 'task' in msg:
                return True  # Will be handled with special filter in extract
            return True

        return False

    def _is_update_task(self, msg: str) -> bool:
        """Check if message is updating a task."""
        update_keywords = ['update', 'change', 'edit', 'modify', 'rename']
        return any(kw in msg for kw in update_keywords)

    def _extract_task_reference(self, msg: str) -> Dict[str, Any]:
        """Extract task ID or reference from message."""
        entities = {}

        # Special case: Batch delete of completed tasks
        # "delete completed tasks", "delete all completed tasks", "remove done tasks"
        if any(kw in msg for kw in ['delete', 'remove']):
            if ('completed' in msg or 'done' in msg or 'finished' in msg) and 'task' in msg:
                # This is a batch operation request
                entities['batch_delete'] = True
                entities['filter_completed'] = True
                return entities

        # Extract numeric task ID (various formats)
        # "task 5", "id 20", "task id20", "#42", "task20", "task3"
        patterns = [
            r'\bid\s*(\d+)',           # "id 20", "id20"
            r'\btask\s*id\s*(\d+)',    # "task id 20", "task id20"
            r'\btask\s+(\d+)',         # "task 5", "task 20"
            r'\bnumber\s+(\d+)',       # "number 3"
            r'#(\d+)',                 # "#42"
            r'\btask(\d+)',            # "task20", "task3"
            r'\bid(\d+)',              # "id20", "id3"
            r'(\d+)\s+task',           # "3 task", "5 task"
        ]

        for pattern in patterns:
            match = re.search(pattern, msg)
            if match:
                entities['task_id'] = int(match.group(1))
                return entities

        # Extract text reference (everything after keywords)
        # "mark test the bot as completed" -> extract "test the bot"
        # "delete buy groceries" -> extract "buy groceries"
        for keyword in ['delete', 'remove', 'complete', 'done', 'mark', 'finish']:
            if keyword in msg:
                # Get text after keyword
                parts = msg.split(keyword, 1)
                if len(parts) > 1:
                    ref_text = parts[1].strip()

                    # Remove status phrases AFTER extracting (as completed, as done, etc.)
                    ref_text = re.sub(r'\s+as\s+(completed?|done|finished?)\s*$', '', ref_text, flags=re.IGNORECASE).strip()

                    # Remove leading "task" or "my task" if present
                    ref_text = re.sub(r'^\s*(the\s+)?task\s+', '', ref_text, flags=re.IGNORECASE).strip()
                    ref_text = re.sub(r'^\s*my\s+task\s+', '', ref_text, flags=re.IGNORECASE).strip()

                    # Keep everything else including "the", "a", etc. (they might be part of task title)
                    if ref_text and len(ref_text) > 2:
                        entities['task_reference'] = ref_text
                        return entities

        return entities

    def _extract_create_entities(self, msg: str) -> Dict[str, Any]:
        """Extract title and metadata for task creation."""
        entities = {}

        # Extract title (text after "add task", "create", "remind me to", etc.)
        patterns = [
            r'add\s+(?:a\s+|new\s+)?task\s+(?:to\s+)?(.+)',  # "add task", "add a task", "add new task", "add task to X"
            r'create\s+(?:a\s+|new\s+)?(?:\d+\s+)?task(?:s)?\s+(?:for\s+|to\s+)?(.+)',  # "create task", "create 5 tasks for X"
            r'make\s+(?:a\s+|new\s+|\d+\s+)?task(?:s)?\s+(?:for\s+|to\s+)?(.+)',  # "make task", "make 5 tasks for X"
            r'remind\s+me\s+to\s+(.+)',  # "remind me to X"
            r'new\s+task(?:s)?\s+(?:for\s+)?(.+)',  # "new tasks for X"
            r'add\s+new\s+task\s*(?::\s*)?(.+)',  # "add new task: X" or "add new task X"
            r'(?:add|create)\s+(?:task\s+)?(.+)',  # Fallback: "add X", "create X" (very flexible)
        ]

        title_text = ""
        for pattern in patterns:
            match = re.search(pattern, msg, re.IGNORECASE)
            if match:
                title_text = match.group(1).strip()
                # Skip if extracted text is too short or just a number
                if len(title_text) > 2 and not title_text.isdigit():
                    break

        # Clean up title (remove date, tag, priority keywords)
        if title_text:
            # Remove tag phrases from title (most specific first)
            title_text = re.sub(r'\bwith\s+tags?\s+"[^"]+"\s*', '', title_text, flags=re.IGNORECASE)
            title_text = re.sub(r'\btags?\s+"[^"]+"\s*', '', title_text, flags=re.IGNORECASE)
            title_text = re.sub(r'\bwith\s+tags?\s+\w+\s*', '', title_text, flags=re.IGNORECASE)
            title_text = re.sub(r'\btags?\s+\w+\s*', '', title_text, flags=re.IGNORECASE)

            # Remove priority phrases from title
            title_text = re.sub(r'\bas\s+(high|medium|low)\s+priority\b', '', title_text, flags=re.IGNORECASE)

            # Remove due date phrases from title
            title_text = re.sub(r'\bdue\s+date\s+tomorrow\b', '', title_text, flags=re.IGNORECASE)
            title_text = re.sub(r'\bdue\s+date\s+today\b', '', title_text, flags=re.IGNORECASE)
            title_text = re.sub(r'\b(tomorrow|today|next week|this week)\b', '', title_text, flags=re.IGNORECASE)

            # Remove date patterns from title (DD MM YYYY)
            title_text = re.sub(r'\bdate\s+\d{1,2}\s+\d{1,2}\s+(?:and\s+)?\d{4}\b', '', title_text, flags=re.IGNORECASE)

            # Clean up quotes and extra whitespace
            title_text = title_text.strip('"\'').strip()
            title_text = re.sub(r'\s+', ' ', title_text)  # Collapse multiple spaces

            if title_text:
                entities['title'] = title_text

        # Extract due date
        due_date = self._extract_due_date(msg)
        if due_date:
            entities['due_date'] = due_date

        # Extract tags
        tags = self._extract_tags(msg)
        if tags:
            entities['tags'] = tags

        # Extract priority
        priority = self._extract_priority(msg)
        if priority:
            entities['priority'] = priority

        return entities

    def _extract_due_date(self, msg: str) -> Optional[str]:
        """Extract due date from message."""
        today = datetime.now()

        # Tomorrow
        if 'tomorrow' in msg:
            due_date = today + timedelta(days=1)
            return due_date.strftime('%Y-%m-%d')

        # Today
        if 'today' in msg or 'todays date' in msg:
            return today.strftime('%Y-%m-%d')

        # Next week
        if 'next week' in msg:
            due_date = today + timedelta(days=7)
            return due_date.strftime('%Y-%m-%d')

        # This week
        if 'this week' in msg:
            # Friday of current week
            days_until_friday = (4 - today.weekday()) % 7
            due_date = today + timedelta(days=days_until_friday)
            return due_date.strftime('%Y-%m-%d')

        # Specific date pattern: "date DD MM YYYY" or "DD/MM/YYYY"
        date_patterns = [
            r'date\s+(\d{1,2})\s+(\d{1,2})\s+(?:and\s+)?(\d{4})',  # "date 29 01 and 2026"
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # "29/01/2026" or "29-01-2026"
        ]

        for pattern in date_patterns:
            match = re.search(pattern, msg)
            if match:
                try:
                    day = int(match.group(1))
                    month = int(match.group(2))
                    year = int(match.group(3))
                    due_date = datetime(year, month, day)
                    return due_date.strftime('%Y-%m-%d')
                except ValueError:
                    pass  # Invalid date

        return None

    def _extract_tags(self, msg: str) -> Optional[List[str]]:
        """Extract tags from message."""
        tags = []

        # Pattern: with tag "X" or tag "X"
        tag_patterns = [
            r'with\s+tags?\s+"([^"]+)"',
            r'tags?\s+"([^"]+)"',
            r'with\s+tags?\s+(\w+)',  # without quotes
            r'tags?\s+(\w+)',  # without quotes
        ]

        for pattern in tag_patterns:
            matches = re.findall(pattern, msg, re.IGNORECASE)
            for match in matches:
                # Split comma-separated tags
                for tag in match.split(','):
                    tag = tag.strip()
                    if tag and tag not in tags:
                        tags.append(tag)

        return tags if tags else None

    def _extract_priority(self, msg: str) -> Optional[str]:
        """Extract priority from message."""
        if 'high priority' in msg or 'urgent' in msg or 'important' in msg or 'as high' in msg:
            return 'high'
        elif 'low priority' in msg or 'as low' in msg:
            return 'low'
        elif 'medium priority' in msg or 'as medium' in msg:
            return 'medium'
        return None

    def _extract_update_entities(self, msg: str) -> Dict[str, Any]:
        """Extract entities for task update."""
        entities = {}

        # Extract task reference from the message
        # Patterns: "update moving phase 4", "update task 5", "update id 20"

        # First, try to extract task ID
        patterns = [
            r'\bid\s*(\d+)',           # "id 20"
            r'\btask\s*id\s*(\d+)',    # "task id 20"
            r'\btask\s+(\d+)',         # "task 5"
        ]

        for pattern in patterns:
            match = re.search(pattern, msg)
            if match:
                entities['task_id'] = int(match.group(1))
                break

        # If no ID found, extract task reference by title
        # Look for text between "update" and "with"/"to"/"as"
        if 'task_id' not in entities:
            # Pattern: "update <task_reference> with/to/as..."
            for keyword in ['with', 'to', 'as', 'due']:
                if keyword in msg:
                    parts = msg.split(keyword, 1)
                    before_keyword = parts[0]
                    # Remove "update" and "task" keywords
                    ref_text = re.sub(r'\b(update|task|the|a|an|my)\b', '', before_keyword).strip()
                    if ref_text and len(ref_text) > 2:
                        entities['task_reference'] = ref_text
                        break

        # Extract description (text after "with description" or "description")
        if 'with description' in msg:
            parts = msg.split('with description', 1)
            if len(parts) > 1:
                desc_text = parts[1].strip()
                # Remove quotes if present
                desc_text = desc_text.strip('"\'')
                # Remove other attributes from description
                desc_text = re.sub(r'\b(due date|tomorrow|today|with tag|priority)\b.*', '', desc_text, flags=re.IGNORECASE).strip()
                if desc_text:
                    entities['description'] = desc_text
        elif 'description' in msg and 'with' not in msg:
            parts = msg.split('description', 1)
            if len(parts) > 1:
                desc_text = parts[1].strip()
                desc_text = desc_text.strip('"\'')
                desc_text = re.sub(r'\b(due date|tomorrow|today|with tag|priority)\b.*', '', desc_text, flags=re.IGNORECASE).strip()
                if desc_text:
                    entities['description'] = desc_text

        # Extract new title (text after "to" but not part of description)
        if ' to ' in msg and 'description' not in msg and 'due' not in msg:
            parts = msg.split(' to ', 1)
            if len(parts) > 1:
                new_title = parts[1].strip()
                # Remove other attributes from title
                new_title = re.sub(r'\b(due date|tomorrow|today|with tag|priority)\b.*', '', new_title, flags=re.IGNORECASE).strip()
                if new_title:
                    entities['title'] = new_title

        # Extract due date
        due_date = self._extract_due_date(msg)
        if due_date:
            entities['due_date'] = due_date

        # Extract tags
        tags = self._extract_tags(msg)
        if tags:
            entities['tags'] = tags

        # Extract priority
        priority = self._extract_priority(msg)
        if priority:
            entities['priority'] = priority

        return entities

    def _extract_list_filters(self, msg: str) -> Dict[str, Any]:
        """Extract filters for task listing."""
        entities = {}

        if 'completed' in msg or 'done' in msg or 'finished' in msg:
            entities['filter_completed'] = True
        elif 'pending' in msg or 'active' in msg or 'todo' in msg:
            entities['filter_completed'] = False

        if 'urgent' in msg or 'high priority' in msg:
            entities['priority'] = 'high'

        return entities
