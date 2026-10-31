if (!['bash', 'editor'].includes(call.type)) {
  throw new Error(`Tool ${call.type} not allowed in minimal harness`);
}
