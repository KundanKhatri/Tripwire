"use client";

import { useState } from "react";
import { ShieldHalf, ArrowDown, Github } from "lucide-react";
import { AttackComposer } from "@/components/AttackComposer";
import { GlassBox } from "@/components/GlassBox";
import { defend } from "@/lib/api";
import { DefendResponse, LAYER_META, LayerName } from "@/lib/types";

const LAYER_ORDER: LayerName[] = [
  "L1_semantic_firewall",
  "L2_capability_provenance",
  "L3_canary_tokens",
  "L4_behavioral_anomaly",
  "L5_learning_classifier",
];

export default function Home() {
  const [result, setResult] = useState<DefendResponse | null>(null);
  const [source, setSource] = useState<"azure" | "local" | null>(null);
  const [busy, setBusy] = useState(false);
  const [stats, setStats] = useState({ tried: 0, blocked: 0 });

  async function handleAttack(payload: string) {
    setBusy(true);
    const { data, source } = await defend(payload);
    setResult(data);
    setSource(source);
    setStats((s) => ({
      tried: s.tried + 1,
      blocked: s.blocked + (data.verdict === "block" ? 1 : 0),
    }));
    setBusy(false);
  }

  return (
    <main className="relative min-h-screen">
      {/* Nav */}
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2">
          <ShieldHalf className="h-6 w-6 text-accent" />
          <span className="font-mono text-lg font-bold tracking-tight">TripWire</span>
        </div>
        <a
          href="https://github.com/KundanKhatri/Tripwire"
          target="_blank"
          rel="noreferrer"
          className="flex items-center gap-2 rounded-lg border border-ink-600 px-3 py-1.5 text-sm text-white/70 transition hover:text-white"
        >
          <Github className="h-4 w-4" /> Repo
        </a>
      </nav>

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 pb-8 pt-10 text-center">
        <div className="reveal mx-auto max-w-3xl">
          <span className="inline-block rounded-full border border-accent/30 bg-accent/10 px-3 py-1 font-mono text-xs text-accent">
            Microsoft Build AI 2026 · Security in the Agentic Future
          </span>
          <h1 className="mt-6 text-balance text-4xl font-bold leading-tight tracking-tight sm:text-5xl">
            Your AI agent is one prompt away from a breach.
            <span className="grad-text"> TripWire stops it.</span>
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-white/60">
            A 5-layer prompt-injection and exfiltration defense for agentic systems, built on Azure.
            Don&apos;t take our word for it — <span className="text-white/90">try to break it yourself.</span>
          </p>
          <a
            href="#arena"
            className="mt-7 inline-flex items-center gap-2 rounded-lg bg-accent px-5 py-3 font-semibold text-ink-950 shadow-glow transition hover:bg-accent-glow"
          >
            Enter the arena <ArrowDown className="h-4 w-4" />
          </a>
        </div>
      </section>

      {/* Arena */}
      <section id="arena" className="mx-auto max-w-6xl px-6 py-12">
        <div className="reveal reveal-1 mb-6 flex items-end justify-between">
          <div>
            <h2 className="text-2xl font-semibold">Live red-team arena</h2>
            <p className="text-sm text-white/50">
              Every payload runs the full defense pipeline. Watch each layer decide.
            </p>
          </div>
          <div className="flex gap-6 text-right">
            <div>
              <p className="tabular font-mono text-2xl font-bold">{stats.tried}</p>
              <p className="text-xs text-white/40">attacks tried</p>
            </div>
            <div>
              <p className="tabular font-mono text-2xl font-bold text-block">{stats.blocked}</p>
              <p className="text-xs text-white/40">blocked</p>
            </div>
          </div>
        </div>

        <div className="reveal reveal-2 grid gap-5 lg:grid-cols-2">
          <AttackComposer onSubmit={handleAttack} busy={busy} />
          <GlassBox result={result} source={source} busy={busy} />
        </div>
      </section>

      {/* Layers */}
      <section className="mx-auto max-w-6xl px-6 py-12">
        <h2 className="reveal mb-2 text-2xl font-semibold">Defense in depth — 5 layers</h2>
        <p className="reveal mb-6 max-w-2xl text-sm text-white/50">
          Microsoft ships the firewall (Prompt Shields). We build the fortress around it. Each layer
          catches a class of attack the others can&apos;t.
        </p>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {LAYER_ORDER.map((name, i) => {
            const meta = LAYER_META[name];
            return (
              <div
                key={name}
                className={`reveal reveal-${Math.min(i + 1, 5)} card-lift rounded-xl border border-ink-600 bg-ink-900/60 p-5`}
              >
                <span className="grid h-9 w-9 place-items-center rounded-lg bg-accent/15 font-mono text-sm font-bold text-accent">
                  {meta.short}
                </span>
                <h3 className="mt-3 font-medium">{meta.label.split("·")[1]?.trim()}</h3>
                <p className="mt-1.5 text-sm leading-relaxed text-white/55">{meta.blurb}</p>
              </div>
            );
          })}
        </div>
      </section>

      <footer className="mx-auto max-w-6xl px-6 py-10 text-center text-xs text-white/30">
        Built solo for Microsoft Build AI 2026 · Azure OpenAI · Content Safety · Container Apps ·
        Cosmos pgvector
      </footer>
    </main>
  );
}
