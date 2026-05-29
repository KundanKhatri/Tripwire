"use client";

import { motion } from "framer-motion";
import { LayerResult, LAYER_META } from "@/lib/types";
import { VerdictBadge } from "./VerdictBadge";
import { cn } from "@/lib/cn";

export function LayerTrace({ layers }: { layers: LayerResult[] }) {
  return (
    <div className="space-y-2">
      {layers.map((l, i) => {
        const meta = LAYER_META[l.layer];
        const dim = l.verdict === "allow";
        return (
          <motion.div
            key={l.layer}
            initial={{ opacity: 0, x: -8 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.08 }}
            className={cn(
              "rounded-lg border border-ink-600 bg-ink-800/60 p-3",
              !dim && "border-l-2",
              l.verdict === "block" && "border-l-block",
              l.verdict === "review" && "border-l-review"
            )}
          >
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <span
                  className={cn(
                    "grid h-7 w-7 place-items-center rounded-md font-mono text-xs font-bold",
                    dim ? "bg-ink-700 text-white/40" : "bg-accent/20 text-accent"
                  )}
                >
                  {meta.short}
                </span>
                <div>
                  <p className={cn("text-sm font-medium", dim && "text-white/55")}>{meta.label}</p>
                  <p className="text-xs text-white/35">{l.latency_ms.toFixed(2)} ms</p>
                </div>
              </div>
              <VerdictBadge verdict={l.verdict} />
            </div>
            {l.reason && (
              <p className="mt-2 pl-10 text-xs text-white/60">
                <span className="text-white/40">reason:</span> {l.reason}
              </p>
            )}
          </motion.div>
        );
      })}
    </div>
  );
}
