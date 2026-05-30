"use client";

import { motion, AnimatePresence } from "framer-motion";
import { DefendResponse } from "@/lib/types";
import { VerdictBadge } from "./VerdictBadge";
import { LayerTrace } from "./LayerTrace";
import { Eye } from "lucide-react";

export function GlassBox({
  result,
  source,
  busy,
}: {
  result: DefendResponse | null;
  source: "azure" | "local" | null;
  busy?: boolean;
}) {
  return (
    <div
      className={`relative overflow-hidden rounded-xl border border-ink-600 bg-ink-900/70 p-5 backdrop-blur ${
        busy ? "scanline" : ""
      }`}
    >
      <div className="mb-4 flex items-center justify-between">
        <div className="flex items-center gap-2 text-sm font-medium text-white/70">
          <Eye className="h-4 w-4 text-accent" />
          Glass Box — defense trace
        </div>
        {source && (
          <span className="rounded-full border border-ink-600 px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-white/40">
            {source === "azure" ? "azure engine" : "local mirror"}
          </span>
        )}
      </div>

      <AnimatePresence mode="wait">
        {!result ? (
          <div
            key="empty"
            className="grid place-items-center py-16 text-center text-sm text-white/35"
          >
            Submit an attack to see every layer&apos;s decision, in order, with latency.
          </div>
        ) : (
          <motion.div key={result.request_id} initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <div className="mb-4 flex items-center justify-between rounded-lg bg-ink-800/80 p-3">
              <span className="text-sm text-white/60">Final verdict</span>
              <VerdictBadge verdict={result.verdict} large />
            </div>
            {result.explanation && (
              <p className="mb-4 rounded-lg border border-ink-600 bg-ink-800/40 p-3 text-sm leading-relaxed text-white/75">
                {result.explanation}
              </p>
            )}
            <LayerTrace layers={result.layers} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
