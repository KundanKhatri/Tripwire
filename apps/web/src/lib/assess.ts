// Client for the Test-Your-Agent security assessment + lead capture.
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "";

export type Verdict = "allow" | "review" | "block";

export interface AttackResult {
  attack_type: string;
  attack_class: "action" | "prompt";
  payload_preview: string;
  tripwire_verdict: Verdict;
  tripwire_reason: string | null;
  agent_exposed: boolean;
}

export interface AssessResponse {
  agent_name: string;
  exposure_grade: string;
  protected_grade: string;
  exposed_count: number;
  total_attacks: number;
  tripwire_caught: number;
  weaknesses: string[];
  strengths: string[];
  attacks: AttackResult[];
  summary: string;
}

export interface AssessInput {
  system_prompt: string;
  tools: string[];
  agent_name: string;
}

const ASSESS_TIMEOUT_MS = 20000;

export async function assessAgent(input: AssessInput): Promise<AssessResponse> {
  if (!API_BASE) throw new Error("Assessment service is not configured.");
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ASSESS_TIMEOUT_MS);
  try {
    const res = await fetch(`${API_BASE}/assess`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
      signal: controller.signal,
    });
    if (!res.ok) throw new Error(`Assessment failed (${res.status}).`);
    return (await res.json()) as AssessResponse;
  } finally {
    clearTimeout(timer);
  }
}

export interface LeadInput {
  email: string;
  agent_context?: string;
  message?: string;
  grade?: string;
}

export async function submitLead(input: LeadInput): Promise<{ ok: boolean; error?: string }> {
  if (!API_BASE) return { ok: false, error: "Lead service is not configured." };
  try {
    const res = await fetch(`${API_BASE}/lead`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...input, source: "test-your-agent" }),
    });
    if (!res.ok) return { ok: false, error: `Submission failed (${res.status}).` };
    return (await res.json()) as { ok: boolean; error?: string };
  } catch {
    return { ok: false, error: "Network error — please email kundanlm10@gmail.com directly." };
  }
}
