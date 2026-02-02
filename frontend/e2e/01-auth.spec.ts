import { test, expect } from '@playwright/test';

/**
 * E2E Test Suite: Authentication Flow
 * Critical: User signup, login, logout
 */

// Generate unique test user credentials
const testUser = {
  name: 'E2E Test User',
  email: `e2e.test.${Date.now()}@example.com`,
  password: 'SecurePass123!',
};

test.describe('Authentication Flow', () => {
  test('should complete full signup flow', async ({ page }) => {
    // Navigate to homepage
    await page.goto('/');

    // Click Sign Up button
    await page.click('text=Sign Up');

    // Wait for signup form
    await expect(page).toHaveURL(/.*signup/);

    // Fill signup form
    await page.fill('input[name="name"]', testUser.name);
    await page.fill('input[type="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.fill('input[name="confirmPassword"]', testUser.password);

    // Submit form
    await page.click('button[type="submit"]');

    // Verify redirect to dashboard
    await expect(page).toHaveURL(/.*dashboard/, { timeout: 10000 });

    // Verify no console errors
    const errors: string[] = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    // Wait a bit to catch any errors
    await page.waitForTimeout(2000);

    expect(errors).toHaveLength(0);
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[type="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/.*dashboard/);

    // Find and click logout button
    // Adjust selector based on your UI
    await page.click('button:has-text("Logout"), [aria-label="Logout"]');

    // Verify redirect to login/homepage
    await expect(page).toHaveURL(/.*login|^\/$/, { timeout: 5000 });

    // Verify cannot access dashboard without auth
    await page.goto('/dashboard');
    await expect(page).toHaveURL(/.*login/, { timeout: 5000 });
  });

  test('should login with valid credentials', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[type="email"]', testUser.email);
    await page.fill('input[name="password"]', testUser.password);
    await page.click('button[type="submit"]');

    // Verify successful login
    await expect(page).toHaveURL(/.*dashboard/, { timeout: 10000 });
  });

  test('should reject invalid login', async ({ page }) => {
    await page.goto('/login');

    await page.fill('input[type="email"]', testUser.email);
    await page.fill('input[name="password"]', 'WrongPassword123!');
    await page.click('button[type="submit"]');

    // Should stay on login page
    await expect(page).toHaveURL(/.*login/);

    // Should show error message
    await expect(page.locator('text=/invalid|incorrect|wrong/i')).toBeVisible({
      timeout: 5000,
    });
  });
});
