import { test, expect } from '@playwright/test';

/**
 * E2E Test Suite: AI Chatbot Interface
 * CRITICAL: Phase III core functionality
 */

const testUser = {
  email: `e2e.chatbot.${Date.now()}@example.com`,
  password: 'SecurePass123!',
};

test.describe('AI Chatbot Interface', () => {
  test.beforeEach(async ({ page }) => {
    // Signup new user for clean state
    await page.goto('/signup');
    await page.fill('input[name="name"]', 'Chatbot Test User');
    await page.fill('input[type="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.fill('input[name="confirmPassword"]', testUser.password);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);

    // Navigate to chat interface
    await page.goto('/dashboard/chat'); // Adjust URL as needed
    // Or click chat button/link
    await page.click('a:has-text("Chat"), button:has-text("Chat"), [href*="chat"]').catch(() => {});
  });

  test('should create task via chat', async ({ page }) => {
    const startTime = Date.now();

    // Find chat input
    const chatInput = page.locator('textarea[placeholder*="message" i], input[placeholder*="message" i]').first();

    // Type message
    await chatInput.fill('add task buy groceries tomorrow');

    // Send message
    await page.click('button:has-text("Send"), button[type="submit"]');

    // Wait for AI response
    await expect(page.locator('text=/created|added|task.*buy groceries/i')).toBeVisible({
      timeout: 10000,
    });

    // Verify response time < 5 seconds
    const responseTime = Date.now() - startTime;
    expect(responseTime).toBeLessThan(5000);

    // Navigate to task list
    await page.goto('/dashboard');

    // Verify task appears
    await expect(page.locator('text=buy groceries')).toBeVisible({ timeout: 5000 });
  });

  test('should list tasks via chat', async ({ page }) => {
    // Create a task first
    const chatInput = page.locator('textarea[placeholder*="message" i], input[placeholder*="message" i]').first();
    await chatInput.fill('add task test task for listing');
    await page.click('button:has-text("Send")');
    await page.waitForTimeout(2000);

    // Clear input
    await chatInput.fill('');

    // Ask to list tasks
    await chatInput.fill('show my tasks');
    await page.click('button:has-text("Send")');

    // Verify response includes task
    await expect(page.locator('text=/test task for listing/i')).toBeVisible({
      timeout: 10000,
    });
  });

  test('should complete task via chat', async ({ page }) => {
    // Create a task
    const chatInput = page.locator('textarea[placeholder*="message" i], input[placeholder*="message" i]').first();
    await chatInput.fill('add task task to mark complete');
    await page.click('button:has-text("Send")');
    await page.waitForTimeout(2000);

    // Clear and send complete command
    await chatInput.fill('mark task 1 as done');
    await page.click('button:has-text("Send")');

    // Verify completion response
    await expect(page.locator('text=/completed|marked.*done|finished/i')).toBeVisible({
      timeout: 10000,
    });

    // Verify in task list
    await page.goto('/dashboard');
    const taskRow = page.locator('text=task to mark complete').locator('..');
    await expect(taskRow.locator('[data-completed="true"], .completed')).toBeVisible().catch(() => {
      return expect(taskRow).toHaveCSS('text-decoration', /line-through/);
    });
  });

  test('should update task via chat', async ({ page }) => {
    // Create a task
    const chatInput = page.locator('textarea[placeholder*="message" i], input[placeholder*="message" i]').first();
    await chatInput.fill('add task original task name');
    await page.click('button:has-text("Send")');
    await page.waitForTimeout(2000);

    // Update task
    await chatInput.fill('update task 1 to updated task name');
    await page.click('button:has-text("Send")');

    // Verify update response
    await expect(page.locator('text=/updated|changed/i')).toBeVisible({
      timeout: 10000,
    });

    // Verify in task list
    await page.goto('/dashboard');
    await expect(page.locator('text=updated task name')).toBeVisible();
  });

  test('should delete task via chat', async ({ page }) => {
    // Create a task
    const chatInput = page.locator('textarea[placeholder*="message" i], input[placeholder*="message" i]').first();
    await chatInput.fill('add task task to delete');
    await page.click('button:has-text("Send")');
    await page.waitForTimeout(2000);

    // Delete task
    await chatInput.fill('delete task 1');
    await page.click('button:has-text("Send")');

    // Verify deletion response
    await expect(page.locator('text=/deleted|removed/i')).toBeVisible({
      timeout: 10000,
    });

    // Verify task removed from list
    await page.goto('/dashboard');
    await expect(page.locator('text=task to delete')).not.toBeVisible();
  });

  test('should handle invalid chat input gracefully', async ({ page }) => {
    const chatInput = page.locator('textarea[placeholder*="message" i], input[placeholder*="message" i]').first();

    // Send gibberish
    await chatInput.fill('asdfjkl;asdfjkl;');
    await page.click('button:has-text("Send")');

    // Should get a response (not crash)
    await expect(page.locator('[data-role="assistant"], .message:has-text("sorry"), .message:has-text("help")')).toBeVisible({
      timeout: 10000,
    });

    // Check for no 500 errors in console
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error' && msg.text().includes('500')) {
        errors.push(msg.text());
      }
    });

    await page.waitForTimeout(1000);
    expect(errors).toHaveLength(0);
  });

  test('should meet performance SLA (<5s response)', async ({ page }) => {
    const chatInput = page.locator('textarea[placeholder*="message" i], input[placeholder*="message" i]').first();

    const responseTimes: number[] = [];

    // Test 5 consecutive messages
    for (let i = 0; i < 5; i++) {
      const startTime = Date.now();

      await chatInput.fill(`add task performance test ${i + 1}`);
      await page.click('button:has-text("Send")');

      await expect(page.locator(`text=/task.*performance test ${i + 1}|created/i`)).toBeVisible({
        timeout: 10000,
      });

      const responseTime = Date.now() - startTime;
      responseTimes.push(responseTime);

      await page.waitForTimeout(500); // Small delay between requests
    }

    // Calculate p95 (5th element when sorted)
    responseTimes.sort((a, b) => a - b);
    const p95 = responseTimes[Math.floor(responseTimes.length * 0.95)];

    console.log('Response times:', responseTimes);
    console.log('p95 latency:', p95, 'ms');

    // Verify p95 < 5000ms
    expect(p95).toBeLessThan(5000);
  });
});
