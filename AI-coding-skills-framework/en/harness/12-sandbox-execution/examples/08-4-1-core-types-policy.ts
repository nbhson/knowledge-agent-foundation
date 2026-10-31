export type RiskTier = "read" | "write" | "elevated" | "prod-auth";

export interface SandboxPolicy {
  workdir: string;              // jail root; must be under an approved base dir
  allowRead: string[];          // extra read-only binds
  allowWrite: string[];         // extra read-write binds
  allowNet: string[];           // [] means no network
  timeoutMs: number;            // hard deadline
  idleMs?: number;              // no-output deadline
  memory: string;               // e.g. "512m"
  cpus: string;                 // e.g. "1.0"
  pids: number;                 // e.g. 64
  env: Record<string, string>;  // already validated
  tier: RiskTier;
  image: string;                // pinned by digest
  runtime?: "runc" | "runsc";  // gVisor opt-in
}

export interface SandboxResult {
  stdout: string;
  stderr: string;
  code: number;
  durationMs: number;
  timedOut: boolean;
  truncated: { stdout: number; stderr: number };
  redactions: number;
  networkBlocked: boolean;
}

export type SandboxErrorCode =
  | "secret-env-denied" | "path-escape" | "deadline-exceeded" | "idle-timeout"
  | "output-cap-exceeded" | "spawn-failed" | "policy-violation" | "image-missing";
