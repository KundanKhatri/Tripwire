import { localDefend } from "./localEngine";
import { DefendResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "";

// Fail over to the local mirror if Azure doesn't answer quickly (cold start,
// hiccup, or network) so the arena is always snappy and never breaks.
const API_TIMEOUT_MS = 6000;

// When the Azure-backed API is configured, call it. Otherwise fall back to the
// local engine so the arena is always interactive (live demo never breaks).
export async function defend(payload: string): Promise<{ data: DefendResponse; source: "azure" | "local" }> {
  if (API_BASE) {
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), API_TIMEOUT_MS);
      const res = await fetch(`${API_BASE}/defend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ payload }),
        signal: controller.signal,
      });
      clearTimeout(timer);
      if (res.ok) {
        return { data: (await res.json()) as DefendResponse, source: "azure" };
      }
    } catch {
      // fall through to local
    }
  }
  // Local mirror — slight delay to feel real.
  await new Promise((r) => setTimeout(r, 220));
  return { data: localDefend(payload), source: "local" };
}
