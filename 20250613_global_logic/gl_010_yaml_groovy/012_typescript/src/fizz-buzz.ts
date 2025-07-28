/**
 * Fizz Buzz app.
 */

/**
 * fizz_buzz function.
 */
export function fizzBuzz(n: number): string {
  let result = '';
  if (n % 3 === 0) {
    result += 'Fizz';
  }
  if (n % 5 === 0) {
    result += 'Buzz';
  }
  return result || n.toString();
}

/**
 * Main function to run fizz_buzz for 1-100.
 */
export function main(): void {
  for (let i = 1; i <= 100; i++) {
    console.log(fizzBuzz(i));
  }
}

// Run when executed directly (ES module check)
if (process.argv[1] && process.argv[1].endsWith('fizz-buzz.ts')) {
  main();
}