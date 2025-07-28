/**
 * Hello Global Logic app.
 */

/**
 * Hello Global Logic function.
 */
export function hello(): void {
  console.log('Hello Global Logic!');
}

// Run when executed directly (ES module check)
if (process.argv[1] && process.argv[1].endsWith('hello-global-logic.ts')) {
  hello();
}