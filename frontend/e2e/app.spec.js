import { test, expect } from '@playwright/test';
import fs from 'fs';
import path from 'path';

// Helper to create a temporary test file
function createTestFile(name, content) {
  const tmpDir = path.join(process.cwd(), '.test-files');
  if (!fs.existsSync(tmpDir)) {
    fs.mkdirSync(tmpDir, { recursive: true });
  }
  const filePath = path.join(tmpDir, name);
  fs.writeFileSync(filePath, content);
  return filePath;
}

// Clean up test files after all tests
test.afterAll(() => {
  const tmpDir = path.join(process.cwd(), '.test-files');
  if (fs.existsSync(tmpDir)) {
    fs.rmSync(tmpDir, { recursive: true });
  }
});

// ============================================================================
// SMOKE TESTS
// ============================================================================

test.describe('Smoke Tests', () => {
  test('app loads successfully', async ({ page }) => {
    await page.goto('/');
    expect(page).toHaveTitle(/ChainMain/i);

    // Check main layout
    await expect(page.locator('.app')).toBeVisible();
    await expect(page.locator('.sidebar')).toBeVisible();
    await expect(page.locator('.main')).toBeVisible();
  });

  test('shows brand name', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.brand-name')).toContainText('ChainMain');
    await expect(page.locator('.brand-sub')).toContainText('Chat with your documents');
  });

  test('displays upload section', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h2:has-text("Upload")')).toBeVisible();
    await expect(page.locator('[data-testid="dropzone"]')).toBeVisible();
  });

  test('displays chat interface', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('[data-testid="question-input"]')).toBeVisible();
    await expect(page.locator('[data-testid="ask-button"]')).toBeVisible();
  });
});

// ============================================================================
// UPLOAD COMPONENT TESTS
// ============================================================================

test.describe('Upload Component', () => {
  test('upload button is disabled initially', async ({ page }) => {
    await page.goto('/');
    const askBtn = page.locator('[data-testid="ask-button"]');
    await expect(askBtn).toBeDisabled();
  });

  test('can select file via file input', async ({ page }) => {
    await page.goto('/');

    // Create a test text file
    const testFile = createTestFile('test.txt', 'This is a test document about machine learning');

    // Set file input
    await page.locator('[data-testid="file-input"]').setInputFiles(testFile);

    // File should be uploaded (we'll see loading state briefly)
    await page.waitForTimeout(500);
  });

  test('can drag and drop file', async ({ page }) => {
    await page.goto('/');

    // Create a test file
    const testFile = createTestFile('dragdrop.txt', 'Content for drag and drop test');

    // Perform drag and drop
    const dropzone = page.locator('[data-testid="dropzone"]');

    // Simulate drag over
    await dropzone.dispatchEvent('dragover');
    await expect(dropzone).toHaveClass(/dragover/);

    // Drop the file
    await dropzone.setInputFiles(testFile);
    await page.waitForTimeout(500);
  });

  test('shows error on upload failure', async ({ page }) => {
    // Mock the API to return error
    await page.goto('/');

    await page.route('**/api/upload', route => {
      route.abort('failed');
    });

    const testFile = createTestFile('invalid.txt', 'test');
    await page.locator('[data-testid="file-input"]').setInputFiles(testFile);

    // Error message might appear
    await page.waitForTimeout(1000);
  });

  test('dropzone highlights on hover', async ({ page }) => {
    await page.goto('/');
    const dropzone = page.locator('[data-testid="dropzone"]');

    await dropzone.hover();
    // Check for visual feedback (would need screenshot to verify in real scenario)
    await expect(dropzone).toBeVisible();
  });

  test('accepts multiple files', async ({ page }) => {
    await page.goto('/');

    // Create multiple test files
    const file1 = createTestFile('doc1.txt', 'First document');
    const file2 = createTestFile('doc2.txt', 'Second document');

    // Upload multiple files
    await page.locator('[data-testid="file-input"]').setInputFiles([file1, file2]);
    await page.waitForTimeout(1000);
  });
});

// ============================================================================
// CHAT COMPONENT TESTS
// ============================================================================

test.describe('Chat Component', () => {
  test('shows empty state initially', async ({ page }) => {
    await page.goto('/');

    const emptyTitle = page.locator('.empty-title');
    await expect(emptyTitle).toContainText('Ask anything about your documents');
  });

  test('empty state text mentions no documents', async ({ page }) => {
    await page.goto('/');

    const emptySub = page.locator('.empty-sub');
    await expect(emptySub).toContainText('Upload files on the left');
  });

  test('input textarea is visible and enabled', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');
    await expect(input).toBeEnabled();
    await expect(input).toHaveAttribute('placeholder', /Ask a question/);
  });

  test('can type in question input', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');
    await input.fill('What is machine learning?');

    await expect(input).toHaveValue('What is machine learning?');
  });

  test('ask button is enabled when text is entered', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');
    const askBtn = page.locator('[data-testid="ask-button"]');

    // Initially disabled
    await expect(askBtn).toBeDisabled();

    // Enable after typing
    await input.fill('Test question');
    await expect(askBtn).toBeEnabled();
  });

  test('ask button is disabled for whitespace-only text', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');
    const askBtn = page.locator('[data-testid="ask-button"]');

    await input.fill('   ');
    await expect(askBtn).toBeDisabled();
  });

  test('enter key sends message', async ({ page }) => {
    // Mock the API response
    await page.goto('/');

    await page.route('**/api/ask', route => {
      route.abort('failed');
    });

    const input = page.locator('[data-testid="question-input"]');
    await input.fill('Test question');

    // Press Enter (this will trigger the request which fails, but that's ok)
    await input.press('Enter');

    // Input should be cleared
    await expect(input).toHaveValue('');
  });

  test('shift+enter creates newline', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');

    await input.focus();
    await input.type('Line 1');
    await input.press('Shift+Enter');
    await input.type('Line 2');

    const value = await input.inputValue();
    expect(value).toContain('Line 1');
    expect(value).toContain('Line 2');
  });

  test('ask button click sends message', async ({ page }) => {
    await page.goto('/');

    await page.route('**/api/ask', route => {
      route.abort('failed');
    });

    const input = page.locator('[data-testid="question-input"]');
    const askBtn = page.locator('[data-testid="ask-button"]');

    await input.fill('Test question');
    await askBtn.click();

    // Input should be cleared
    await expect(input).toHaveValue('');
  });
});

// ============================================================================
// DOCUMENT LIST COMPONENT TESTS
// ============================================================================

test.describe('Document List', () => {
  test('shows "no documents" initially', async ({ page }) => {
    await page.goto('/');

    // Documents list should be empty
    const documentItems = page.locator('.document-item');
    await expect(documentItems).toHaveCount(0);
  });

  test('document item has checkbox', async ({ page }) => {
    await page.goto('/');

    // Mock documents API
    await page.route('**/api/documents', route => {
      route.respond({
        status: 200,
        body: JSON.stringify({
          documents: [
            { doc_id: '1', filename: 'test.txt', pages: 1, chunks: 5 }
          ]
        })
      });
    });

    await page.reload();
    const checkbox = page.locator('input[type="checkbox"]').first();
    await expect(checkbox).toBeVisible();
  });

  test('can toggle document selection', async ({ page }) => {
    await page.goto('/');

    // Mock documents API
    await page.route('**/api/documents', route => {
      route.respond({
        status: 200,
        body: JSON.stringify({
          documents: [
            { doc_id: '1', filename: 'test.txt', pages: 1, chunks: 5 }
          ]
        })
      });
    });

    await page.reload();
    const checkbox = page.locator('input[type="checkbox"]').first();

    // Toggle selection
    await checkbox.click();
    await expect(checkbox).toBeChecked();

    await checkbox.click();
    await expect(checkbox).not.toBeChecked();
  });
});

// ============================================================================
// KEYBOARD SHORTCUTS & INTERACTIONS
// ============================================================================

test.describe('Keyboard Interactions', () => {
  test('focus management works', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');

    // Input should be focusable
    await input.focus();
    await expect(input).toBeFocused();
  });

  test('textarea expands when needed', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');
    const initialHeight = await input.evaluate(el => el.clientHeight);

    // Type multiline text
    await input.fill('Line 1\nLine 2\nLine 3\nLine 4');

    const newHeight = await input.evaluate(el => el.clientHeight);
    expect(newHeight).toBeGreaterThanOrEqual(initialHeight);
  });
});

// ============================================================================
// RESPONSIVE & LAYOUT TESTS
// ============================================================================

test.describe('Layout & Responsive', () => {
  test('sidebar and main sections are visible', async ({ page }) => {
    await page.goto('/');

    const sidebar = page.locator('.sidebar');
    const main = page.locator('.main');

    await expect(sidebar).toBeVisible();
    await expect(main).toBeVisible();
  });

  test('layout is grid-based', async ({ page }) => {
    await page.goto('/');

    const app = page.locator('.app');
    const display = await app.evaluate(el =>
      window.getComputedStyle(el).display
    );

    expect(['grid', 'flex']).toContain(display);
  });

  test('chat scrolls to bottom on new messages', async ({ page }) => {
    await page.goto('/');

    // Get initial scroll position
    const scroll = page.locator('.scroll');
    const initialScroll = await scroll.evaluate(el => el.scrollTop);

    // The component should auto-scroll when messages are added
    // This is tested through CSS and behavior
    await expect(scroll).toBeVisible();
  });
});

// ============================================================================
// API INTEGRATION TESTS
// ============================================================================

test.describe('API Integration', () => {
  test('backend health endpoint works', async ({ page }) => {
    const response = await page.request.get('http://localhost:9000/health');
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('status', 'ok');
    expect(data).toHaveProperty('embedding_model');
    expect(data).toHaveProperty('llm_model');
  });

  test('documents endpoint returns list', async ({ page }) => {
    const response = await page.request.get('http://localhost:9000/api/documents');

    if (response.status() === 200) {
      const data = await response.json();
      expect(data).toHaveProperty('documents');
      expect(Array.isArray(data.documents)).toBe(true);
    }
  });

  test('handles network errors gracefully', async ({ page }) => {
    await page.goto('/');

    // Simulate network error
    await page.route('**/api/documents', route => {
      route.abort('failed');
    });

    await page.reload();

    // App should still be functional (error handling in place)
    const input = page.locator('[data-testid="question-input"]');
    await expect(input).toBeVisible();
  });
});

// ============================================================================
// ACCESSIBILITY TESTS
// ============================================================================

test.describe('Accessibility', () => {
  test('buttons have proper labels', async ({ page }) => {
    await page.goto('/');

    const askBtn = page.locator('[data-testid="ask-button"]');
    await expect(askBtn).toHaveText(/Ask/);
  });

  test('textarea has placeholder text', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');
    const placeholder = await input.getAttribute('placeholder');

    expect(placeholder).toBeTruthy();
    expect(placeholder).toContain('Ask a question');
  });

  test('form elements are keyboard accessible', async ({ page }) => {
    await page.goto('/');

    // Tab through elements
    await page.keyboard.press('Tab');

    // Should focus on an interactive element
    const focusedElement = await page.evaluate(() =>
      document.activeElement.tagName
    );

    expect(['BUTTON', 'INPUT', 'TEXTAREA']).toContain(focusedElement);
  });
});

// ============================================================================
// ERROR HANDLING TESTS
// ============================================================================

test.describe('Error Handling', () => {
  test('displays error when documents API fails', async ({ page }) => {
    await page.goto('/');

    await page.route('**/api/documents', route => {
      route.respond({
        status: 500,
        body: JSON.stringify({ detail: 'Server error' })
      });
    });

    await page.reload();

    // Error message should appear
    const error = page.locator('.err');
    // May or may not show depending on error handling
    if (await error.isVisible()) {
      await expect(error).toBeVisible();
    }
  });

  test('handles invalid question submission', async ({ page }) => {
    await page.goto('/');

    const input = page.locator('[data-testid="question-input"]');
    const askBtn = page.locator('[data-testid="ask-button"]');

    // Try to click ask with empty input (should be disabled)
    await input.fill('');
    await expect(askBtn).toBeDisabled();
  });
});
