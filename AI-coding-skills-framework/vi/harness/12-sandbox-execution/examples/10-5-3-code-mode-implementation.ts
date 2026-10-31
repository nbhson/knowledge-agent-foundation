import { runSandboxed, SandboxError, type SandboxPolicy } from "./sandbox";

export interface CodeModeProgram {
  ts: string;
  entry: string;              // tên hàm async được export
  tier: SandboxPolicy["tier"];
}

/** Chương trình chạy bên trong sandbox. Nó CHỈ có thể tới tool qua proxy
 *  bên dưới — proxy này enforce cap và gate. Không mạng, không fs, không env. */
export async function runCodeMode(prog: CodeModeProgram, policy: SandboxPolicy) {
  const proxy = `// bootstrap được tiêm vào
import { parentPort } from "node:worker_threads";
declare const __call: (tool: string, args: unknown) => Promise<unknown>;
(globalThis as any).__call = (t, a) => parentPort!.postMessage({ kind: "call", t, a });
`;
  // 1. Pre-flight: chương trình gọi tool nào? (quét tĩnh + log proxy lúc chạy)
  const detected = /__call\(\s*["']([\w.]+)["']/g;
  const tools = new Set<string>();
  for (const m of prog.ts.matchAll(detected)) tools.add(m[1]!);

  // 2. Gate TRƯỚC khi thực thi, không phải sau
  for (const t of tools) {
    const verdict = await gatekeeper.request({ tier: riskOf(t, prog.tier), summary: `code-mode:${t}`, /* … */ });
    if (verdict !== "approved") return { ok: false, blocked: t, verdict };
  }

  // 3. Chạy trong sandbox; mạng tắt nên proxy là đường egress duy nhất
  const r = await runSandboxed(
    ["node", "--experimental-vm-modules", "/app/runner.mjs"],
    ["/app/bundle.js", prog.entry],
    { ...policy, allowNet: [], env: { PATH: "/usr/bin" } },
  );
  if (r.code !== 0) return { ok: false, error: r.stderr || r.stdout };

  // 4. Kết quả tool quay về qua host proxy, cap và gate riêng từng cái
  const results = await Promise.all(pending.map(c =>
    callTool(c.t, c.a).then(v => ({ ...v, text: JSON.stringify(v).slice(0, 128_000) }))));
  return { ok: true, stdout: r.stdout, results };
}
