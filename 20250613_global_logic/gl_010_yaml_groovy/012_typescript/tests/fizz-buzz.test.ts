/**
 * Tests for fizz-buzz module.
 */

import { fizzBuzz } from '../src/fizz-buzz';

describe('fizz-buzz', () => {
  it('should return number for non-multiples', () => {
    expect(fizzBuzz(1)).toBe('1');
    expect(fizzBuzz(2)).toBe('2');
    expect(fizzBuzz(4)).toBe('4');
    expect(fizzBuzz(7)).toBe('7');
    expect(fizzBuzz(11)).toBe('11');
  });

  it('should return "Fizz" for multiples of 3', () => {
    expect(fizzBuzz(3)).toBe('Fizz');
    expect(fizzBuzz(6)).toBe('Fizz');
    expect(fizzBuzz(9)).toBe('Fizz');
    expect(fizzBuzz(12)).toBe('Fizz');
  });

  it('should return "Buzz" for multiples of 5', () => {
    expect(fizzBuzz(5)).toBe('Buzz');
    expect(fizzBuzz(10)).toBe('Buzz');
    expect(fizzBuzz(20)).toBe('Buzz');
    expect(fizzBuzz(25)).toBe('Buzz');
  });

  it('should return "FizzBuzz" for multiples of 15', () => {
    expect(fizzBuzz(15)).toBe('FizzBuzz');
    expect(fizzBuzz(30)).toBe('FizzBuzz');
    expect(fizzBuzz(45)).toBe('FizzBuzz');
    expect(fizzBuzz(60)).toBe('FizzBuzz');
  });

  it('should handle edge cases', () => {
    expect(fizzBuzz(0)).toBe('FizzBuzz');
    expect(fizzBuzz(-3)).toBe('Fizz');
    expect(fizzBuzz(-5)).toBe('Buzz');
    expect(fizzBuzz(-15)).toBe('FizzBuzz');
  });

  it('should have correct type signature', () => {
    const result = fizzBuzz(1);
    expect(typeof result).toBe('string');
  });
});