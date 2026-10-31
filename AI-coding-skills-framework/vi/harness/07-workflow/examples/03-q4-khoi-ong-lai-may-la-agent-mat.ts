this.ckpt({ runId, key, status: "ok",
            val: JSON.stringify(out).slice(0, 64_000), at: Date.now() });
