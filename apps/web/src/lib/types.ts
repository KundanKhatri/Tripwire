export type Verdict = "allow" | "review" | "block";

export type LayerName =
  | "L1_semantic_firewall"
  | "L2_capability_provenance"
  | "L3_canary_tokens"
  | "L4_behavioral_anomaly"
  | "L5_learning_classifier";

export interface LayerResult {
  layer: LayerName;
  verdict: Verdict;
  confidence: number;
  latency_ms: number;
  signals: Record<string, unknown>;
  reason: string | null;
}

export interface DefendResponse {
  request_id: string;
  verdict: Verdict;
  layers: LayerResult[];
  explanation: string | null;
  created_at: string;
}

export const LAYER_META: Record<LayerName, { label: string; short: string; blurb: string }> = {
  L1_semantic_firewall: {
    label: "L1 · Semantic Firewall",
    short: "L1",
    blurb: "Prompt Shields + pattern rules + embedding similarity to a known-attack corpus.",
  },
  L2_capability_provenance: {
    label: "L2 · Capability Provenance",
    short: "L2",
    blurb: "Signed tokens prove which user input authorized each tool call. No token, no action.",
  },
  L3_canary_tokens: {
    label: "L3 · Canary Tokens",
    short: "L3",
    blurb: "Decoy secrets seeded into context. If one ever leaves, it is proof of exfiltration.",
  },
  L4_behavioral_anomaly: {
    label: "L4 · Behavioral Anomaly",
    short: "L4",
    blurb: "Embeds the action vs. the user goal. Divergence means goal hijack.",
  },
  L5_learning_classifier: {
    label: "L5 · Learning Classifier",
    short: "L5",
    blurb: "A model fine-tuned on the live corpus. Gets stronger every time it is attacked.",
  },
};
