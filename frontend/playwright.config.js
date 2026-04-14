import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for ChainMain E2E tests
 * Runs against http://localhost:9001 (frontend) and http://localhost:9000 (API)
 *
 * Usage:
 *   npm run test:e2e          # Run tests headless
 *   npm run test:e2e:ui       # Run with UI (visual debugging)
 *   npx playwright test --debug  # Run with Playwright Inspector
 *   npx playwright test --headed  # Run in headed mode (see browser)
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  timeout: 30 * 1000,
  expect: {
    timeout: 5000,
  },

  use: {
    baseURL: 'http://localhost:9001',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],

  // Start dev server before tests
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:9001',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
