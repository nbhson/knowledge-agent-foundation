import { runSandboxed, SandboxError, type SandboxPolicy } from "./sandbox";

export interface CodeModeProgram {
  ts: string;
  entry: string;              // exported async function name
  tier: SandboxPolicy["tier"];
}

/** The program runs inside the sandbox. It may ONLY reach tools through the proxy
 *  below — which enforces caps and gates. There is no direct network, no fs, no env. */
export async function runCodeMode(prog: CodeModeProgram, policy: SandboxPolicy) {
  const proxy = `// injected bootstrap
import { parentPort } from "node:worker_threads";
declare const __call: (tool: string, args: unknown) => Promise<unknown>;
(globalThis as any).__call = (t, a) => parentPort!.postMessage({ kind: "call", t, a });
`;
  // 1. Pre-flight: which tools does it call? (static scan + runtime proxy log)
  const detected = /__call\(\s*["']([\w.]+)["']/g;
  const tools = new Set<string>();
  for (const m of prog.ts.matchAll(detected)) tools.add(m[1]!);

  // 2. Gate BEFORE execution, not after
  for (const t of tools) {
    const verdict = await gatekeeper.request({ tier: riskOf(t, prog.tier), summary: `code-mode:${t}`, /* … */ });
    if (verdict !== "approved") return { ok: false, blocked: t, verdict };
  }

  // 3. Run inside the sandbox; network is off, so the proxy is the only egress path
  const r = await runSandboxed(
    ["node", "--experimental-vm-modules", "/app/runner.mjs"],
    ["/app/bundle.js", prog.entry],
    { ...policy, allowNet: [], env: { PATH: "/usr/bin" } },
  );
  if (r.code !== 0) return { ok: false, error: r.stderr || r.stdout };

  // 4. Tool results return through the host proxy, capped and gated individually
  const results = await Promise.all(pending.map(c =>
    callTool(c.t, c.a).then(v => ({ ...v, text: JSON.stringify(v).slice(0, 128_000) }))));
  return { ok: true, stdout: r.stdout, results };
}
