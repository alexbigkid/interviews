/**
 * Tests for meta-data module.
 */

import {
  processMetadataItem,
  handleProcessingError,
  logProgress,
  onCompleted,
  onError,
  main,
  metadataList,
} from '../src/meta-data';

// Mock console.log
const mockConsoleLog = jest.fn();
console.log = mockConsoleLog;

// Mock Math.random
const mockMathRandom = jest.fn();
Math.random = mockMathRandom;

// Mock setTimeout
const mockSetTimeout = jest.fn();
global.setTimeout = mockSetTimeout as any;

// Mock clearTimeout
const mockClearTimeout = jest.fn();
global.clearTimeout = mockClearTimeout as any;

describe('meta-data', () => {
  beforeEach(() => {
    mockConsoleLog.mockClear();
    mockMathRandom.mockClear();
    mockSetTimeout.mockClear();
    mockClearTimeout.mockClear();
  });

  describe('processMetadataItem', () => {
    it('should process metadata item successfully', async () => {
      const metadata = { id: 1, value: 'Item 1' };
      
      mockMathRandom.mockReturnValue(0.5); // Success case
      // Mock setTimeout to resolve immediately
      mockSetTimeout.mockImplementation((callback: Function) => {
        callback();
        return 123;
      });
      
      const result = await processMetadataItem(metadata);
      expect(result).toBe('Processed Item 1');
    });

    it('should throw error for failure case', async () => {
      const metadata = { id: 1, value: 'Item 1' };
      
      mockMathRandom.mockReturnValue(0.1); // Failure case
      
      await expect(processMetadataItem(metadata)).rejects.toThrow('Failed to process');
    });
  });

  describe('handleProcessingError', () => {
    it('should log error and return empty observable', (done) => {
      const error = new Error('Test error');
      const metadata = { id: 1, value: 'Item 1' };

      const result = handleProcessingError(error, metadata);
      
      result.subscribe({
        next: () => {
          throw new Error('Should not emit any values');
        },
        complete: () => {
          expect(mockConsoleLog).toHaveBeenCalledWith(
            expect.stringContaining('💣 [Error Handler]')
          );
          expect(mockConsoleLog).toHaveBeenCalledWith(
            expect.stringContaining('Test error')
          );
          done();
        },
      });
    });
  });

  describe('logProgress', () => {
    it('should log progress message', () => {
      const result = 'Test progress message';
      
      logProgress(result);
      
      expect(mockConsoleLog).toHaveBeenCalledWith('🚀 [Progress] Test progress message');
    });
  });

  describe('onCompleted', () => {
    it('should log completion message', () => {
      onCompleted();
      
      expect(mockConsoleLog).toHaveBeenCalledWith('✅ All metadata processed.');
    });
  });

  describe('onError', () => {
    it('should log error message', () => {
      const error = new Error('Test error');
      
      onError(error);
      
      expect(mockConsoleLog).toHaveBeenCalledWith('💣 ❌ Stream failed: Test error');
    });
  });

  describe('metadataList', () => {
    it('should be properly initialized', () => {
      expect(metadataList).toHaveLength(10);
      expect(metadataList[0]).toEqual({ id: 0, value: 'Item 0' });
      expect(metadataList[9]).toEqual({ id: 9, value: 'Item 9' });
    });

    it('should have correct structure', () => {
      metadataList.forEach((item) => {
        expect(item).toHaveProperty('id');
        expect(item).toHaveProperty('value');
        expect(typeof item.id).toBe('number');
        expect(typeof item.value).toBe('string');
        expect(item.value).toMatch(/^Item \d+$/);
      });
    });
  });

  describe('main', () => {
    it('should set up timeout correctly', () => {
      // Mock successful processing
      mockMathRandom.mockReturnValue(0.5);
      
      // Mock setTimeout to not execute callback
      mockSetTimeout.mockImplementation((_callback: Function, _delay: number) => {
        return 123; // return a timer ID
      });
      
      // Start main but don't await it
      main();
      
      // Verify timeout was set up
      expect(mockSetTimeout).toHaveBeenCalledWith(expect.any(Function), 30000);
    });

    it('should handle timeout scenario', async () => {
      // Mock successful processing
      mockMathRandom.mockReturnValue(0.5);
      
      // Mock setTimeout to immediately call the timeout callback
      mockSetTimeout.mockImplementation((callback: Function, _delay: number) => {
        callback(); // Immediately trigger timeout
        return 123;
      });
      
      await main();
      
      expect(mockConsoleLog).toHaveBeenCalledWith(
        '💣 ❌ Timed out waiting for all processing to complete.'
      );
    });
  });
});