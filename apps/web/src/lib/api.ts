import { localDefend } from "./localEngine";
import { DefendResponse } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "";

// When the Azure-backed API is configured, call it. Otherwise fall back to the
// local engine so the arena is always interactive (live demo never breaks).
export async function defend(payload: string): Promise<{ data: DefendResponse; source: "azure" | "local" }> {
  if (API_BASE) {
    try {
      const res = await fetch(`${API_BASE}/defend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ payload }),
      });
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
