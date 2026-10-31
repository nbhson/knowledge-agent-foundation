import { appendFile, open, mkdir } from "node:fs/promises";
import { join } from "node:path";
import { ulid } from "ulid";
import { redactPayload, TrajectoryEventSchema } from "./schema";

const FSYNC_KINDS = new Set(["approval_verdict", "memory_write", "eval", "session_start", "session_end"]);
const MAX_PAYLOAD = 64_000;

export class TrajectoryStore {
  private seq = 0;
  private buffer: string[] = [];
  private timer?: NodeJS.Timeout;
  dropped = 0; lastError?: unknown; currentSession = "";

  constructor(private root: string) {}

  /** Mọi module gọi hàm này. Không bao giờ throw vào vòng lặp agent —
   *  một lỗi telemetry không được làm hỏng task. Lỗi được đếm và báo. */
  async append(e: Omit<TrajectoryEvent, "id" | "seq">): Promise<void> {
    try {
      const { payload, redactions } = redactPayload(e.payload);
      const ev = TrajectoryEventSchema.parse({
        ...e, id: `evt_${ulid()}`, seq: this.seq++, redactions,
        payload: JSON.stringify(payload).length > MAX_PAYLOAD ? { ref: blobRef(payload) } : payload,
      });
      const line = JSON.stringify(ev) + "\n";
      if (FSYNC_KINDS.has(ev.kind)) {
        await this.flush();
        const fh = await open(this.path(ev.sessionId), "a");
        await fh.appendFile(line); await fh.sync(); await fh.close();
      } else {
        this.buffer.push(line);
        this.timer ??= setTimeout(() => void this.flush(), 100);
      }
    } catch (err) { this.dropped++; this.lastError = err; }
  }

  async flush(): Promise<void> {
    clearTimeout(this.timer); this.timer = undefined;
    if (!this.buffer.length) return;
    const b = this.buffer; this.buffer = [];
    await mkdir(this.root, { recursive: true });
    await appendFile(this.path(this.currentSession), b.join(""), "utf8");
  }

  async close(): Promise<void> { await this.flush(); }
  path(sessionId: string) { return join(this.root, `${sessionId}.jsonl`); }
}
