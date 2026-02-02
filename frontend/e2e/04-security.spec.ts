import { test, expect } from '@playwright/test';

/**
 * E2E Test Suite: User Isolation & Security
 * CRITICAL: Verify users cannot access each other's data
 */

const user1 = {
  name: 'User One',
  email: `user1.${Date.now()}@example.com`,
  password: 'SecurePass123!',
};

const user2 = {
  name: 'User Two',
  email: `user2.${Date.now()}@example.com`,
  password: 'SecurePass123!',
};

test.describe('User Isolation & Security', () => {
  test('should enforce user isolation for tasks', async ({ page }) => {
    // Create User 1 and add task
    await page.goto('/signup');
    await page.fill('input[name="name"]', user1.name);
    await page.fill('input[type="email"]', user1.email);
    await page.fill('input[name="password"]', user1.password);
    await page.fill('input[name="confirmPassword"]', user1.password);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);

    // Create task as User 1
    await page.keyboard.press('n');
    await page.fill('input[name="title"], input[placeholder*="task" i]', 'User 1 Private Task');
    await page.click('button[type="submit"]');
    await expect(page.locator('text=User 1 Private Task')).toBeVisible();

    // Logout User 1
    await page.click('button:has-text("Logout"), [aria-label="Logout"]');
    await expect(page).toHaveURL(/.*login|^\//);

    // Create User 2
    await page.goto('/signup');
    await page.fill('input[name="name"]', user2.name);
    await page.fill('input[type="email"]', user2.email);
    await page.fill('input[name="password"]', user2.password);
    await page.fill('input[name="confirmPassword"]', user2.password);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);

    // Verify User 2 cannot see User 1's task
    await expect(page.locator('text=User 1 Private Task')).not.toBeVisible();

    // Create task as User 2
    await page.keyboard.press('n');
    await page.fill('input[name="title"], input[placeholder*="task" i]', 'User 2 Private Task');
    await page.click('button[type="submit"]');

    // Verify User 2 only sees own task
    await expect(page.locator('text=User 2 Private Task')).toBeVisible();
    await expect(page.locator('text=User 1 Private Task')).not.toBeVisible();
  });

  test('should enforce user isolation in chatbot', async ({ page }) => {
    // Login as User 1
    await page.goto('/login');
    await page.fill('input[type="email"]', user1.email);
    await page.fill('input[name="password"]', user1.password);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);

    // Navigate to chat
    await page.goto('/dashboard/chat').catch(() => {});
    await page.click('a:has-text("Chat"), [href*="chat"]').catch(() => {});

    // Ask chatbot for tasks
    const chatInput = page.locator('textarea[placeholder*="message" i], input[placeholder*="message" i]').first();
    await chatInput.fill('show all my tasks');
    await page.click('button:has-text("Send")');

    // Verify only User 1's tasks shown
    await expect(page.locator('text=User 1 Private Task')).toBeVisible({
      timeout: 10000,
    });
    await expect(page.locator('text=User 2 Private Task')).not.toBeVisible();

    // Logout
    await page.goto('/dashboard');
    await page.click('button:has-text("Logout")');

    // Login as User 2
    await page.goto('/login');
    await page.fill('input[type="email"]', user2.email);
    await page.fill('input[name="password"]', user2.password);
    await page.click('button[type="submit"]');

    // Navigate to chat
    await page.goto('/dashboard/chat').catch(() => {});
    await page.click('a:has-text("Chat"), [href*="chat"]').catch(() => {});

    // Ask chatbot for tasks
    await chatInput.fill('show all my tasks');
    await page.click('button:has-text("Send")');
    await page.waitForTimeout(2000);

    // Verify only User 2's tasks shown
    await expect(page.locator('text=User 2 Private Task')).toBeVisible({
      timeout: 10000,
    });
    await expect(page.locator('text=User 1 Private Task')).not.toBeVisible();
  });

  test('should require authentication for protected routes', async ({ page }) => {
    // Attempt to access dashboard without login
    await page.goto('/dashboard');

    // Should redirect to login
    await expect(page).toHaveURL(/.*login/, { timeout: 5000 });

    // Attempt to access chat without login
    await page.goto('/dashboard/chat');

    // Should redirect to login
    await expect(page).toHaveURL(/.*login/, { timeout: 5000 });
  });

  test('should have no critical console errors during normal usage', async ({ page }) => {
    const criticalErrors: string[] = [];

    // Listen for console errors
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        const text = msg.text();
        // Filter out known non-critical warnings
        if (!text.includes('google.generativeai') && !text.includes('DevTools')) {
          criticalErrors.push(text);
        }
      }
    });

    // Login
    await page.goto('/login');
    await page.fill('input[type="email"]', user1.email);
    await page.fill('input[name="password"]', user1.password);
    await page.click('button[type="submit"]');

    // Create task
    await page.keyboard.press('n');
    await page.fill('input[name="title"]', 'Console Error Test');
    await page.click('button[type="submit"]');

    // Use chatbot
    await page.goto('/dashboard/chat').catch(() => {});
    const chatInput = page.locator('textarea[placeholder*="message" i]').first();
    await chatInput.fill('show my tasks');
    await page.click('button:has-text("Send")');
    await page.waitForTimeout(3000);

    // Verify no critical errors
    console.log('Critical errors found:', criticalErrors);
    expect(criticalErrors).toHaveLength(0);
  });
});
