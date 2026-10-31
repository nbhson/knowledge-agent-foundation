import { z } from "zod";

export const TrajectoryEventSchema = z.object({
  id: z.string().regex(/^evt_[0-9A-HJKMNP-TV-Z]{26}$/),  // ULID
  seq: z.number().int().nonnegative(),
  sessionId: z.string().min(1),
  parentTaskId: z.string().optional(),
  runId: z.string().optional(),
  ts: z.number().int(),
  kind: z.enum([/* … */]),
  actor: z.string().min(1),
  payload: z.unknown(),
  tokens: z.object({ in: z.number(), out: z.number(), cached: z.number().optional() }).optional(),
  latencyMs: z.number().nonnegative().optional(),
  model: z.string().optional(),
  costUsd: z.number().nonnegative().optional(),
  error: z.object({ code: z.string(), retryable: z.boolean() }).optional(),
  fingerprint: z.string().optional(),
}).superRefine((e, ctx) => {
  if (e.kind !== "session_start" && !e.parentTaskId)
    ctx.addIssue({ code: "custom", message: "orphan event: parentTaskId required" });
});
