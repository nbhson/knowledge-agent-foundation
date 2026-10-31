// ── Policy ────────────────────────────────────────────────────────────────
export type RiskTier = "read" | "write" | "elevated" | "prod-auth";

export interface SandboxPolicy {
  workdir: string; allowRead: string[]; allowWrite: string[]; allowNet: string[];
  timeoutMs: number; idleMs?: number; memory: string; cpus: string; pids: number;
  env: Record<string, string>; tier: RiskTier; image: string;
  runtime?: "runc" | "runsc";
}

// ── Result ────────────────────────────────────────────────────────────────
export interface SandboxResult {
  stdout: string; stderr: string; code: number; durationMs: number;
  timedOut: boolean; truncated: { stdout: number; stderr: number };
  redactions: number; networkBlocked: boolean;
}

export type SandboxErrorCode =
  | "secret-env-denied" | "path-escape" | "deadline-exceeded" | "idle-timeout"
  | "output-cap-exceeded" | "spawn-failed" | "policy-violation" | "image-missing";

// ── Executor ──────────────────────────────────────────────────────────────
export interface SandboxExecutor {
  run(cmd: string[], args: string[], policy: SandboxPolicy): Promise<SandboxResult>;
  assertJailed(policy: SandboxPolicy, path: string): Promise<string>;
  hash(policy: SandboxPolicy): string;                     // policyHash để audit
}

// ── Audit ─────────────────────────────────────────────────────────────────
export interface SandboxAuditRecord {
  sessionId: string; taskId: string; toolName: string;
  policyHash: string; tier: RiskTier; runtime: string; image: string;
  argvHash: string; durationMs: number; exitCode: number;
  stdoutBytes: number; redactions: number; denied: SandboxErrorCode | null;
  egress: { host: string; bytes: number }[]; at: number;
}

// ── Supply chain ──────────────────────────────────────────────────────────
export interface ImageManifest {
  ref: string;                          // repo:tag@sha256:…
  digest: string; signatureVerified: boolean; builtAt: number;
  toolchain: string[]; packages: Record<string, string>;   // ghim theo lockfile
  sbom?: string;                        // CycloneDX / SPDX
}

// ── Test surface ──────────────────────────────────────────────────────────
export interface EscapeDrill {
  name: string; argv: string[]; patch?: Partial<SandboxPolicy>;
  expect: SandboxErrorCode | "ok" | `exit-${number}`;
}

export interface SandboxSuite {
  drills: EscapeDrill[];
  run(): Promise<{ total: number; passed: number; failures: EscapeDrill[] }>;
}
