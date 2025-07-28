/**
 * Tests for hello-global-logic module.
 */

import { hello } from '../src/hello-global-logic';

// Mock console.log
const mockConsoleLog = jest.fn();
console.log = mockConsoleLog;

describe('hello-global-logic', () => {
  beforeEach(() => {
    mockConsoleLog.mockClear();
  });

  it('should print correct message', () => {
    hello();
    
    expect(mockConsoleLog).toHaveBeenCalledWith('Hello Global Logic!');
  });

  it('should be a callable function', () => {
    expect(typeof hello).toBe('function');
  });
});