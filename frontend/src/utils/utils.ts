// Helper function for delaying
// https://dev.to/zxce3/implementing-delaysleep-in-javascript-with-promises-and-asyncawait-264
export const simulateNetworkDelay = (ms: number) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};
