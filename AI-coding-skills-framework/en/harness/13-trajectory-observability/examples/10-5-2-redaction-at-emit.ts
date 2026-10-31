const PII = [
  /sk-[A-Za-z0-9_-]{20,}/g,                 // API keys
  /gh[pousr]_\w{20,}/g,                     // GitHub tokens
  /AKIA[0-9A-Z]{16}/g,                      // AWS access key id
  /-----BEGIN [A-Z ]*PRIVATE KEY-----/g,     // private keys
  /[\w.+-]+@[\w-]+\.[\w.]{2,}/g,             // email
  /\b(?:\d[ -]?){13,19}\b/g,                 // card numbers
];

export function redactPayload<T>(payload: T): { payload: T; redactions: number } {
  let s = JSON.stringify(payload), n = 0;
  for (const re of PII) s = s.replace(re, () => { n++; return "[REDACTED]"; });
  return { payload: JSON.parse(s), redactions: n };
}
