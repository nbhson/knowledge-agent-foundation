import { spawn } from "node:child_process";
import { realpath } from "node:fs/promises";
import { isAbsolute, relative, resolve } from "node:path";

const SECRET_ENV  = /^(AWS_|AZURE_|GCP_|GH_|GITHUB_|OPENAI_|ANTHROPIC_|SK_|BEARER_|NPM_TOKEN_)/i;
const SECRET_VAL  = [/sk-[A-Za-z0-9_-]{20,}/g, /ghp_\w{20,}/g, /AKIA[0-9A-Z]{16}/g,
                     /-----BEGIN [A-Z ]*PRIVATE KEY-----/g, /eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}/g];
const OUT_CAP = 256_000, ERR_CAP = 64_000, ARGV_CAP = 32_000;

export class SandboxError extends Error {
  constructor(public code: SandboxErrorCode, msg: string) { super(`${code}: ${msg}`); }
}

/** Control 1 — normalize + jail assertion (defeats .., symlinks, double-encoding).
 *  Under the jail root → allowed (workdir is bind-mounted rw).
 *  Outside it → allowed ONLY via an explicit allowRead/allowWrite bind. */
export async function assertJailed(p: SandboxPolicy, candidate: string): Promise<string> {
  const root = await realpath(p.workdir);
  let abs: string;
  try { abs = await realpath(resolve(root, candidate)); }          // realpath kills symlink + .. +
  catch { throw new SandboxError("path-escape", candidate); }      // double-encoding; missing = escape
  const rel = relative(root, abs);
  if (rel.startsWith("..") || isAbsolute(rel)) {
    const viaBind = [...p.allowRead, ...p.allowWrite].some(m =>
      !relative(resolve(root, m), abs).startsWith(".."));
    if (!viaBind) throw new SandboxError("path-escape", candidate);
  }
  return abs;
}

function redact(s: string): { text: string; count: number } {
  let n = 0;
  for (const re of SECRET_VAL) { s = s.replace(re, () => { n++; return "[REDACTED]"; }); }
  return { text: s, count: n };
}

/** path-shaped argv → host-side guard BEFORE it reaches docker. URLs and flags are
 *  not file paths, so `cat /etc/shadow` / `cat ../../etc/passwd` / `cat ./link/id_rsa`
 *  die here with `path-escape` instead of depending on the container to deny them. */
function isPathArg(tok: string): boolean {
  return tok.startsWith("/") || tok.startsWith(".");
}

export async function runSandboxed(
  cmd: string[], args: string[], p: SandboxPolicy
): Promise<SandboxResult> {
  // Control 5a — prevention
  for (const k of Object.keys(p.env)) if (SECRET_ENV.test(k)) throw new SandboxError("secret-env-denied", k);
  if (JSON.stringify(args).length > ARGV_CAP) throw new SandboxError("policy-violation", "argv cap");

  // Control 1 — guard every path-shaped argv token on the host, before spawning.
  for (const tok of [...cmd, ...args]) if (isPathArg(tok)) await assertJailed(p, tok);

  // Control 1 + 2 — the argv is the sandbox definition
  const docker = [
    "run", "--rm", "--init",
    "--read-only", "--tmpfs", "/tmp:rw,noexec,nosuid,size=64m",
    "--cap-drop=ALL", "--security-opt=no-new-privileges",
    `--pids-limit=${p.pids}`, `--memory=${p.memory}`, `--cpus=${p.cpus}`,
    "--network", p.allowNet.length ? "bridge" : "none",
    "-v", `${p.workdir}:/work:rw`, "-w", "/work", "--tmpfs", "/work/tmp",
    ...p.allowRead.map(m => ["-v", `${m}:${m}:ro`]).flat(),
    ...p.allowWrite.map(m => ["-v", `${m}:${m}:rw`]).flat(),
    ...Object.entries(p.env).map(([k, v]) => ["-e", `${k}=${v}`]).flat(),
  ];
  if (!/@sha256:/.test(p.image)) throw new SandboxError("policy-violation", "pin image by digest");
  const argv = p.runtime === "runsc"
    ? ["--runtime=runsc", "run", ...docker.slice(1), p.image, ...cmd, ...args]
    : [...docker, p.image, ...cmd, ...args];

  return new Promise((resolve, reject) => {
    const started = Date.now();
    let out = "", err = "", lastByte = Date.now();
    // Control 5b — the child gets PATH only, never the supervisor's env
    const c = spawn("docker", argv, { env: { PATH: process.env.PATH ?? "/usr/bin:/bin" },
                                       detached: true, stdio: ["ignore", "pipe", "pipe"] });

    let timer: NodeJS.Timeout, idle: NodeJS.Timeout | null = null;
    // Control 3 — whole process group dies, not just the PID we spawned
    const fail = (e: SandboxError) => {
      clearTimeout(timer); if (idle) clearInterval(idle);
      try { process.kill(-c.pid!, "SIGKILL"); } catch {}
      try { c.kill("SIGKILL"); } catch {}
      reject(e);
    };
    timer = setTimeout(() => fail(new SandboxError("deadline-exceeded", cmd.join(" "))), p.timeoutMs);
    if (p.idleMs) idle = setInterval(() => {
      if (Date.now() - lastByte > p.idleMs!) fail(new SandboxError("idle-timeout", cmd.join(" ")));
    }, 1000);

    c.stdout.on("data", d => {                                   // Control 4 — HARD cap: kill,
      lastByte = Date.now();                                     // never soft-truncate a writer
      out += d.toString();
      if (Buffer.byteLength(out, "utf8") > OUT_CAP) fail(new SandboxError("output-cap-exceeded", cmd.join(" ")));
    });
    c.stderr.on("data", d => {
      lastByte = Date.now();
      err += d.toString();
      if (Buffer.byteLength(err, "utf8") > ERR_CAP) fail(new SandboxError("output-cap-exceeded", cmd.join(" ")));
    });
    c.on("error", e => fail(new SandboxError("spawn-failed", e.message)));
    c.on("close", code => {
      clearTimeout(timer); if (idle) clearInterval(idle);
      const so = redact(out), se = redact(err);                   // Control 5c
      resolve({
        stdout: so.text, stderr: se.text,
        code: code ?? 1, durationMs: Date.now() - started, timedOut: false,
        truncated: { stdout: 0, stderr: 0 },                    // soft caps live at the MCP /
        redactions: so.count + se.count, networkBlocked: p.allowNet.length === 0,  // file-read layer
      });
    });
  });
}
