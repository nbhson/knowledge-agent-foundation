import { runSandboxed, SandboxError, type SandboxPolicy } from "./sandbox";
import { mkdtemp, symlink, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

const IMAGE = "sandbox-img@sha256:9f2c4e1b…";
const base: SandboxPolicy = {
  workdir: "", allowRead: [], allowWrite: [], allowNet: [], timeoutMs: 3000,
  memory: "256m", cpus: "1.0", pids: 64, env: { PATH: "/usr/bin" },
  tier: "write", image: IMAGE,
};

async function drill(name: string, cmd: string[], expect: string, patch: Partial<SandboxPolicy> = {}) {
  const workdir = await mkdtemp(join(tmpdir(), "sbx-"));
  await symlink("/root/.ssh", join(workdir, "link"));           // for drill 6
  let outcome = "ok", detail = "";
  try {
    const r = await runSandboxed(cmd, [], { ...base, workdir, ...patch });
    outcome = r.code === 0 ? "ok" : `exit-${r.code}`;
    detail = r.stdout.slice(0, 80) + r.stderr.slice(0, 80);
  } catch (e) { outcome = e instanceof SandboxError ? e.code : "unknown"; }
  const pass = outcome.startsWith(expect);
  console.log(`${pass ? "PASS" : "FAIL"}  ${name.padEnd(34)} → ${outcome}`);
  if (!pass) console.log(`      expected ${expect}; got ${detail}`);
  await rm(workdir, { recursive: true, force: true });
  return pass;
}

export async function runDrills(): Promise<boolean> {
  const results = await Promise.all([
    drill("echo",                 ["echo", "ok"],                              "ok",                 { timeoutMs: 5000 }),
    drill("sleep deadline",       ["sleep", "60"],                             "deadline-exceeded"),
    drill("backgrounded sleep",   ["bash", "-c", "sleep 60 &"],                 "deadline-exceeded"),
    drill("read /etc/shadow",     ["cat", "/etc/shadow"],                       "path-escape",        { timeoutMs: 2000 }),
    drill("traversal",            ["cat", "../../etc/passwd"],                  "path-escape",        { timeoutMs: 2000 }),
    drill("symlink escape",       ["cat", "./link/id_rsa"],                     "path-escape",        { timeoutMs: 2000 }),
    drill("no secret env",        ["printenv"],                                "ok",                 { timeoutMs: 2000 }),
    drill("net blocked",          ["curl", "-sS", "https://example.com"],       "exit-",              { timeoutMs: 3000 }),
    drill("metadata blocked",     ["curl", "-sS", "http://169.254.169.254/"],   "exit-",              { timeoutMs: 3000 }),
    drill("output cap",           ["yes"],                                     "output-cap-exceeded",{ timeoutMs: 5000 }),
    drill("fork bomb",            ["bash", "-c", "for i in $(seq 1 9999); do sleep 5 & done"], "exit-", { timeoutMs: 4000 }),
    drill("no docker socket",     ["docker", "run", "alpine"],                 "exit-",              { timeoutMs: 3000 }),
    drill("read-only rootfs",     ["sh", "-c", "echo x > /etc/hosts"],         "exit-",              { timeoutMs: 2000 }),
  ]);
  const ok = results.filter(Boolean).length;
  console.log(`\n${ok}/${results.length} drills passed`);
  return ok === results.length;
}
