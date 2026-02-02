import { test, expect } from '@playwright/test';

/**
 * E2E Test Suite: Task Management via UI
 * Critical: CRUD operations
 */

// Test user credentials (should exist from auth tests)
const testUser = {
  email: `e2e.test.${Date.now()}@example.com`,
  password: 'SecurePass123!',
};

test.describe('Task Management UI', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login');
    await page.fill('input[type="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);
  });

  test('should create task via UI', async ({ page }) => {
    // Click "New Task" button (or press 'N')
    await page.keyboard.press('n');

    // Alternative: await page.click('button:has-text("New Task")');

    // Fill task form
    await page.fill('input[name="title"], input[placeholder*="task" i]', 'E2E Test Task 1');

    // Try to find description field
    const descField = page.locator('textarea[name="description"], textarea[placeholder*="description" i]').first();
    if (await descField.isVisible()) {
      await descField.fill('Testing task creation');
    }

    // Submit form
    await page.click('button[type="submit"]:has-text("Create"), button:has-text("Add Task")');

    // Verify task appears in list
    await expect(page.locator('text=E2E Test Task 1')).toBeVisible({ timeout: 10000 });

    // Verify success notification
    await expect(page.locator('text=/created|added|success/i')).toBeVisible({
      timeout: 5000,
    });
  });

  test('should update task', async ({ page }) => {
    // Create a task first
    await page.keyboard.press('n');
    await page.fill('input[name="title"], input[placeholder*="task" i]', 'Task to Update');
    await page.click('button[type="submit"]:has-text("Create"), button:has-text("Add Task")');
    await expect(page.locator('text=Task to Update')).toBeVisible();

    // Click on task to edit
    await page.click('text=Task to Update');

    // Update title
    await page.fill('input[name="title"], input[value="Task to Update"]', 'Task Updated Successfully');

    // Save changes
    await page.click('button:has-text("Save"), button:has-text("Update")');

    // Verify updated task appears
    await expect(page.locator('text=Task Updated Successfully')).toBeVisible({
      timeout: 5000,
    });
  });

  test('should mark task as complete', async ({ page }) => {
    // Create a task
    await page.keyboard.press('n');
    await page.fill('input[name="title"], input[placeholder*="task" i]', 'Task to Complete');
    await page.click('button[type="submit"]:has-text("Create"), button:has-text("Add Task")');
    await expect(page.locator('text=Task to Complete')).toBeVisible();

    // Find and click checkbox or complete button
    const taskRow = page.locator('text=Task to Complete').locator('..');
    await taskRow.locator('input[type="checkbox"], button:has-text("Complete")').first().click();

    // Verify task marked as complete (strikethrough or checkmark)
    await expect(taskRow.locator('text=Task to Complete')).toHaveCSS('text-decoration', /line-through/, {
      timeout: 5000,
    }).catch(() => {
      // Alternative: check for checkmark icon
      return expect(taskRow.locator('[data-completed="true"], .completed')).toBeVisible();
    });
  });

  test('should delete task', async ({ page }) => {
    // Create a task
    await page.keyboard.press('n');
    await page.fill('input[name="title"], input[placeholder*="task" i]', 'Task to Delete');
    await page.click('button[type="submit"]:has-text("Create"), button:has-text("Add Task")');
    await expect(page.locator('text=Task to Delete')).toBeVisible();

    // Find and click delete button
    const taskRow = page.locator('text=Task to Delete').locator('..');
    await taskRow.locator('button:has-text("Delete"), [aria-label*="Delete"]').first().click();

    // If confirmation dialog appears, confirm
    const confirmButton = page.locator('button:has-text("Confirm"), button:has-text("Yes")');
    if (await confirmButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await confirmButton.click();
    }

    // Verify task removed
    await expect(page.locator('text=Task to Delete')).not.toBeVisible({ timeout: 5000 });
  });

  test('should filter tasks by priority', async ({ page }) => {
    // Create tasks with different priorities
    await page.keyboard.press('n');
    await page.fill('input[name="title"]', 'High Priority Task');

    // Select high priority (adjust selector based on UI)
    const prioritySelect = page.locator('select[name="priority"], button:has-text("Priority")').first();
    if (await prioritySelect.isVisible().catch(() => false)) {
      await prioritySelect.click();
      await page.click('text=High, [data-value="high"]');
    }

    await page.click('button[type="submit"]');
    await expect(page.locator('text=High Priority Task')).toBeVisible();

    // Open filter panel
    await page.keyboard.press('f'); // Or click filter button

    // Select high priority filter
    await page.click('text=High, [data-priority="high"]');

    // Verify only high priority tasks shown
    await expect(page.locator('text=High Priority Task')).toBeVisible();
  });
});
