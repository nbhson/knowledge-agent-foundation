export type RiskTier = "read" | "write" | "elevated" | "prod-auth";

export interface SandboxPolicy {
  workdir: string;              // jail root; phải nằm dưới base dir được duyệt
  allowRead: string[];          // bind read-only bổ sung
  allowWrite: string[];         // bind read-write bổ sung
  allowNet: string[];           // [] nghĩa là không có mạng
  timeoutMs: number;            // deadline cứng
  idleMs?: number;              // deadline không-output
  memory: string;               // ví dụ "512m"
  cpus: string;                 // ví dụ "1.0"
  pids: number;                 // ví dụ 64
  env: Record<string, string>;  // đã được validate
  tier: RiskTier;
  image: string;                // ghim bằng digest
  runtime?: "runc" | "runsc";  // bật gVisor
}

export interface SandboxResult {
  stdout: string; stderr: string; code: number;
  durationMs: number; timedOut: boolean;
  truncated: { stdout: number; stderr: number };
  redactions: number; networkBlocked: boolean;
}

export type SandboxErrorCode =
  | "secret-env-denied" | "path-escape" | "deadline-exceeded" | "idle-timeout"
  | "output-cap-exceeded" | "spawn-failed" | "policy-violation" | "image-missing";
