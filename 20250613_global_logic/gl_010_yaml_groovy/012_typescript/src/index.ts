/**
 * Main entry point for gl-012 TypeScript project.
 */

export { hello } from './hello-global-logic.js';
export { fizzBuzz, main as fizzBuzzMain } from './fizz-buzz.js';
export {
  main as metaDataMain,
  processMetadataItem,
  handleProcessingError,
  logProgress,
  onCompleted,
  onError,
  metadataList,
} from './meta-data.js';