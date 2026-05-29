// Local defense engine — a faithful TS mirror of the Python L1 pattern bank.
// Lets the arena demonstrate real blocking with ZERO backend dependency, so the
// site is live and interactive the moment it deploys. When NEXT_PUBLIC_API_BASE
// is set, the API client calls the real Azure-backed engine instead.

import { DefendResponse, LayerResult, Verdict } from "./types";

interface Rule {
  id: string;
  owasp: string;
  re: RegExp;
  severity: number;
}

const RULES: Rule[] = [
  { id: "role_override_ignore", owasp: "LLM01", re: /\bignore\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?)/i, severity: 9 },
  { id: "role_override_disregard", owasp: "LLM01", re: /\b(disregard|forget|override)\s+(your|the)\s+(instructions?|system\s+prompt|guidelines?)/i, severity: 9 },
  { id: "role_override_assistant", owasp: "LLM01", re: /\byou\s+are\s+(now\s+)?(a\s+)?(different|new)\s+(assistant|ai|model)\b/i, severity: 8 },
  { id: "system_prompt_leak", owasp: "LLM01", re: /\b(reveal|show|print|repeat|tell\s+me)\s+(your|the)\s+(system\s+prompt|initial\s+instructions|hidden\s+instructions)/i, severity: 9 },
  { id: "verbatim_request", owasp: "LLM01", re: /\bverbatim\b.{0,40}\b(prompt|instructions|system\s+message)/i, severity: 8 },
  { id: "delimiter_escape", owasp: "LLM01", re: /("""|'''|<\|im_(end|start)\|>|<\/?system>|<\/?assistant>|<\/?user>)/i, severity: 7 },
  { id: "base64_hidden", owasp: "LLM01", re: /\b(decode|base64).{0,40}(execute|run|follow)/i, severity: 8 },
  { id: "tool_force", owasp: "LLM07", re: /\b(call|invoke|execute)\s+(the\s+)?(tool|function|api)\s+\w+\s+(with|using)/i, severity: 6 },
  { id: "exfil_external", owasp: "LLM02", re: /\b(send|post|get|fetch)\b.{0,40}\bhttps?:\/\//i, severity: 7 },
  { id: "exfil_image_md", owasp: "LLM02", re: /!\[[^\]]*\]\(https?:\/\/[^)]+\?[^)]*=[^)]*\)/i, severity: 8 },
  { id: "jailbreak_dan", owasp: "LLM01", re: /\b(DAN|do\s+anything\s+now|developer\s+mode\s+enabled)\b/i, severity: 9 },
  { id: "jailbreak_hypothetical", owasp: "LLM01", re: /\bhypothetically\b.{0,40}\b(unrestricted|no\s+rules|no\s+filter)/i, severity: 7 },
  { id: "agency_grant", owasp: "LLM08", re: /\byou\s+(have|are\s+given)\s+(full|admin|root|sudo)\s+(access|permissions?)/i, severity: 8 },
  { id: "indirect_inject", owasp: "LLM01", re: /(###\s*system\s*###|\[note from admin\]|new instruction:)/i, severity: 9 },
];

const CANARY_PREFIX = "tw-canary-";

function worst(a: Verdict, b: Verdict): Verdict {
  const rank = { allow: 0, review: 1, block: 2 } as const;
  return rank[a] >= rank[b] ? a : b;
}

export function localDefend(payload: string): DefendResponse {
  const layers: LayerResult[] = [];

  // L1 — pattern bank
  const t0 = performance.now();
  const hits = RULES.filter((r) => r.re.test(payload)).map((r) => ({
    id: r.id,
    owasp_class: r.owasp,
    severity: r.severity,
  }));
  const highSev = hits.filter((h) => h.severity >= 8);
  let l1: Verdict = "allow";
  let l1reason: string | null = null;
  let l1conf = 0;
  if (highSev.length) {
    l1 = "block";
    l1conf = 0.9;
    l1reason = `High-severity pattern match: ${highSev[0].id}`;
  } else if (hits.length) {
    l1 = "review";
    l1conf = 0.6;
    l1reason = `Pattern match: ${hits[0].id}`;
  }
  layers.push({
    layer: "L1_semantic_firewall",
    verdict: l1,
    confidence: l1conf,
    latency_ms: Math.round((performance.now() - t0) * 100) / 100,
    signals: { pattern_hits: hits, prompt_shields: { available: false, note: "Azure layer wired server-side" } },
    reason: l1reason,
  });

  // L2 — provenance (no token on arena path)
  layers.push({
    layer: "L2_capability_provenance",
    verdict: "allow",
    confidence: 1,
    latency_ms: 0.01,
    signals: { token_present: false },
    reason: "No capability token on read-only arena path",
  });

  // L3 — canary echo detection
  const canaryEcho = payload.toLowerCase().includes(CANARY_PREFIX);
  layers.push({
    layer: "L3_canary_tokens",
    verdict: canaryEcho ? "block" : "allow",
    confidence: canaryEcho ? 1 : 1,
    latency_ms: 0.02,
    signals: { active_canaries: 3, canary_echo: canaryEcho },
    reason: canaryEcho ? "Canary-prefix token observed in payload (exfil replay)" : null,
  });

  // L4 — coarse anomaly
  const words = payload.trim().split(/\s+/);
  const shortDestructive =
    words.length <= 8 && /\b(delete|drop|exec|execute|rm|shutdown)\b/i.test(payload);
  layers.push({
    layer: "L4_behavioral_anomaly",
    verdict: shortDestructive ? "review" : "allow",
    confidence: shortDestructive ? 0.5 : 0.9,
    latency_ms: 0.04,
    signals: { skeleton: true, tokens: words.length, note: "Embedding divergence wired server-side" },
    reason: shortDestructive ? "Short imperative with destructive verb" : null,
  });

  // L5 — classifier placeholder
  layers.push({
    layer: "L5_learning_classifier",
    verdict: "allow",
    confidence: 0.3,
    latency_ms: 0.01,
    signals: { model_deployed: false },
    reason: "Classifier endpoint deploys on Azure ML (Day 4)",
  });

  const verdict = layers.reduce<Verdict>((acc, l) => worst(acc, l.verdict), "allow");

  return {
    request_id: crypto.randomUUID(),
    verdict,
    layers,
    explanation: explain(verdict, layers),
    created_at: new Date().toISOString(),
  };
}

function explain(verdict: Verdict, layers: LayerResult[]): string {
  const fired = layers.filter((l) => l.verdict !== "allow");
  if (verdict === "allow") {
    return "No layer raised a flag. This input looks like a normal request — it would be passed through to the agent.";
  }
  const lead = fired[0];
  const which = fired.map((f) => f.layer.split("_")[0].toUpperCase()).join(", ");
  if (verdict === "block") {
    return `Blocked. ${which} flagged this. Primary signal: ${lead.reason}. TripWire stopped the request before it reached the agent.`;
  }
  return `Held for review. ${which} raised a soft signal: ${lead.reason}. In production this routes to a human or a stricter model.`;
}
