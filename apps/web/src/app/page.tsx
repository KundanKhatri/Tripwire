"use client";

import { useState } from "react";
import {
  ShieldHalf,
  ArrowDown,
  ArrowRight,
  Github,
  KeyRound,
  Eye,
  FileText,
  Network,
  Fingerprint,
  Gauge,
  Cloud,
  Database,
  Cpu,
  ShieldCheck,
  Sparkles,
  Mail,
  CheckCircle2,
  ShieldAlert,
  Bug,
  Wrench,
  Brain,
  Coins,
  Scale,
} from "lucide-react";
import Link from "next/link";
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

const PROBLEM_STATS = [
  { big: "88%", label: "of organizations have already had an agent-related security incident", color: "text-block" },
  { big: "~6%", label: "of security budget covers agent risk", color: "text-review" },
  { big: "$47K", label: "cost of a single documented runaway agent loop", color: "text-[#b57bff]" },
  { big: "0%", label: "false-positive cost — provenance & canary are zero-FP by construction", color: "text-allow" },
];

const AZURE = [
  { icon: Cpu, name: "Azure OpenAI", sub: "text-embedding-3-large · similarity + anomaly" },
  { icon: ShieldCheck, name: "Azure AI Content Safety", sub: "Prompt Shields — L1 baseline (verified live)" },
  { icon: Cloud, name: "Azure Container Apps", sub: "FastAPI defense engine" },
  { icon: Database, name: "Cosmos DB for PostgreSQL", sub: "pgvector corpus + immutable traces" },
  { icon: Network, name: "Static Web Apps / SignalR", sub: "arena UI + live leaderboard" },
  { icon: ShieldHalf, name: "Bicep + azd", sub: "one-command provisioning (IaC)" },
];

const BUSINESS = [
  {
    icon: Sparkles,
    title: "Model — open-core",
    body: "The OSS engine drives adoption; the enterprise tier sells identity, the compliance audit ledger, and the cross-org trust fabric. Bottom-up, developer-led GTM.",
  },
  {
    icon: Database,
    title: "The moat — compounding data",
    body: "Every blocked attack feeds the learning classifier and the corpus. Data → identity → compliance → network: each layer is harder to copy than the last.",
  },
  {
    icon: Gauge,
    title: "Why now",
    body: "Agent deployments are exploding; EU AI Act penalties begin Aug 2026; incumbents guard the prompt, not the action. The window is open.",
  },
];

const MARKET = [
  { k: "$10.8B → $50B", v: "AI-agent market, 2026 → 2030" },
  { k: "~45–50%", v: "CAGR of the agent-security sub-segment" },
  { k: "Aug 2026", v: "EU AI Act penalties begin — audit demand" },
];

const ROADMAP = [
  { tag: "F1", icon: Fingerprint, name: "Agent Identity Ledger", body: "Cryptographic identity + lifecycle for every agent (NHI)." },
  { tag: "F2", icon: ShieldCheck, name: "MCP Tool Firewall", body: "Defeat tool poisoning & rug-pulls — scan + hash-pin + sandbox." },
  { tag: "F3", icon: Gauge, name: "Cost & Loop Governor", body: "Kill runaway agents before the $47K bill." },
  { tag: "F4", icon: Eye, name: "Memory-Poisoning Shield", body: "Provenance + taint for long-term agent memory." },
  { tag: "F5", icon: FileText, name: "Compliance Audit Ledger", body: "EU AI Act / SOC2-ready signed action trail." },
  { tag: "V1/V2", icon: Network, name: "Trust Fabric + Risk Score", body: "The cross-org network and the data moat." },
];

const SHIPPED = [
  "L1 semantic firewall live on Azure (Prompt Shields + embeddings, verified)",
  "L2 capability provenance + L3 canary tripwires — tested, 13 tests green",
  "Victim-agent demo: indirect injection defeated end-to-end",
  "Live red-team arena with the Glass Box trace viewer",
  "Bicep IaC · honest held-out benchmark · OWASP-mapped attack corpus",
];

const THREATS = [
  {
    icon: Bug,
    pain: "Indirect prompt injection",
    painBody: "Hidden instructions ride in the documents, emails, and web pages your agent reads. The user's request was benign — the attack wasn't in it.",
    answer: "L2 provenance denies any tool call that wasn't authorized by the real user request — the injected instruction has no authority to act.",
  },
  {
    icon: Wrench,
    pain: "Tool poisoning via MCP",
    painBody: "A connected tool's metadata carries malicious instructions, or a trusted tool gets rug-pulled in an update. Your agent inherits the payload.",
    answer: "Scoped capability tokens + (roadmap) hash-pinned tool manifests mean a changed or rogue tool can't silently gain new powers.",
  },
  {
    icon: Brain,
    pain: "Memory poisoning",
    painBody: "False 'facts' planted into long-term memory persist across sessions and quietly steer every future decision the agent makes.",
    answer: "Canary tripwires + provenance on memory writes (roadmap F4) flag untrusted writes and prove when tainted memory tries to act.",
  },
  {
    icon: Coins,
    pain: "Runaway cost loops",
    painBody: "A confused or hijacked agent loops on tool calls and burns a five-figure bill before anyone notices. One documented loop ran 11 days.",
    answer: "Cost & loop governor (roadmap F3) enforces hard per-task budgets and kills the loop before the bill — every action already passes through TripWire.",
  },
  {
    icon: Eye,
    pain: "Silent data exfiltration",
    painBody: "Secrets leave through a rendered image URL, an outbound request, or an email the agent was tricked into sending. You never see it happen.",
    answer: "L3 canaries seed decoy secrets; if one ever crosses the boundary it's hard proof of exfiltration — caught with zero false positives.",
  },
  {
    icon: Scale,
    pain: "No audit trail / compliance gap",
    painBody: "When something goes wrong — or an auditor asks — most teams can't show what their agent actually did. EU AI Act penalties begin Aug 2026.",
    answer: "Every decision produces a signed, replayable trace (Glass Box). The compliance audit ledger (roadmap F5) turns it into SOC2 / EU-AI-Act evidence.",
  },
];

function Anchor({ id }: { id: string }) {
  return <span id={id} className="block -translate-y-20" />;
}

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
      <nav className="sticky top-0 z-40 border-b border-white/5 bg-ink-950/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-3.5">
          <a href="#top" className="flex items-center gap-2">
            <ShieldHalf className="h-6 w-6 text-accent" />
            <span className="font-mono text-lg font-bold tracking-tight">TripWire</span>
          </a>
          <div className="hidden items-center gap-6 text-sm text-white/55 md:flex">
            <a href="#arena" className="transition hover:text-white">Arena</a>
            <a href="#threats" className="transition hover:text-white">Threats</a>
            <a href="#how" className="transition hover:text-white">How it works</a>
            <a href="#business" className="transition hover:text-white">Business</a>
            <a href="#about" className="transition hover:text-white">About</a>
          </div>
          <div className="flex items-center gap-2">
            <Link
              href="/test-your-agent"
              className="hidden rounded-lg bg-accent/15 px-3 py-1.5 text-sm font-medium text-accent transition hover:bg-accent/25 sm:flex"
            >
              Test your agent
            </Link>
            <a
              href="/Tripwire/TripWire_Deck.pdf"
              className="hidden rounded-lg border border-ink-600 px-3 py-1.5 text-sm text-white/70 transition hover:text-white sm:flex"
            >
              Deck
            </a>
            <a
              href="https://github.com/KundanKhatri/Tripwire"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 rounded-lg border border-ink-600 px-3 py-1.5 text-sm text-white/70 transition hover:text-white"
            >
              <Github className="h-4 w-4" /> Repo
            </a>
          </div>
        </div>
      </nav>

      <Anchor id="top" />

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 pb-6 pt-16 text-center">
        <div className="reveal mx-auto max-w-3xl">
          <span className="inline-block rounded-full border border-accent/30 bg-accent/10 px-3 py-1 font-mono text-xs text-accent">
            Microsoft Build AI 2026 · Security in the Agentic Future
          </span>
          <h1 className="mt-6 text-balance text-4xl font-bold leading-[1.1] tracking-tight sm:text-6xl">
            The control plane for
            <span className="grad-text"> AI agent actions.</span>
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-pretty text-lg leading-relaxed text-white/60">
            LLM firewalls inspect the text going <em>in</em>. TripWire governs what an agent is allowed
            to <em>do</em> — stopping prompt injection, tool poisoning, and data exfiltration at the
            action layer. <span className="text-white/90">Don&apos;t take our word for it — try to break it.</span>
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link
              href="/test-your-agent"
              className="glow-pulse inline-flex items-center gap-2 rounded-lg bg-accent px-5 py-3 font-semibold text-ink-950 transition hover:bg-accent-glow"
            >
              <ShieldAlert className="h-4 w-4" /> Test your agent
            </Link>
            <a
              href="#arena"
              className="inline-flex items-center gap-2 rounded-lg border border-ink-600 px-5 py-3 font-semibold text-white/80 transition hover:border-accent/50 hover:text-white"
            >
              Enter the arena <ArrowDown className="h-4 w-4" />
            </a>
          </div>
          <div className="mt-7 flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-xs text-white/40">
            <span className="inline-flex items-center gap-1.5"><CheckCircle2 className="h-3.5 w-3.5 text-allow" /> Live on Azure</span>
            <span className="inline-flex items-center gap-1.5"><CheckCircle2 className="h-3.5 w-3.5 text-allow" /> Open source</span>
            <span className="inline-flex items-center gap-1.5"><CheckCircle2 className="h-3.5 w-3.5 text-allow" /> 13 tests green</span>
            <span className="inline-flex items-center gap-1.5"><CheckCircle2 className="h-3.5 w-3.5 text-allow" /> Honest benchmarks</span>
          </div>
        </div>
      </section>

      {/* Problem stat band */}
      <section className="mx-auto max-w-6xl px-6 py-10">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {PROBLEM_STATS.map((s, i) => (
            <div
              key={s.big}
              className={`reveal reveal-${Math.min(i + 1, 5)} card-lift rounded-xl border border-ink-600 bg-ink-900/60 p-5`}
            >
              <p className={`tabular font-mono text-3xl font-bold ${s.color}`}>{s.big}</p>
              <p className="mt-2 text-sm leading-relaxed text-white/55">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Arena */}
      <Anchor id="arena" />
      <section className="mx-auto max-w-6xl px-6 py-12">
        <div className="reveal mb-6 flex items-end justify-between">
          <div>
            <h2 className="text-2xl font-semibold sm:text-3xl">Live red-team arena</h2>
            <p className="mt-1 text-sm text-white/50">
              Every payload runs the full defense pipeline. Watch each layer decide, in real time.
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

      {/* The insight / moat */}
      <section className="mx-auto max-w-6xl px-6 py-14">
        <div className="reveal mx-auto max-w-3xl text-center">
          <span className="font-mono text-xs uppercase tracking-widest text-accent">The insight</span>
          <h2 className="mt-3 text-2xl font-bold leading-tight sm:text-4xl">
            Don&apos;t try to recognize every attack.
            <br className="hidden sm:block" />
            <span className="grad-text"> Deny it authority. Catch the theft.</span>
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-pretty leading-relaxed text-white/60">
            Indirect injection is unsolvable by text inspection: the user&apos;s request is benign and the
            attack hides in tool-returned content. So we stopped playing whack-a-mole with payloads and
            changed the model of trust.
          </p>
        </div>
        <div className="mt-9 grid gap-5 md:grid-cols-2">
          <div className="reveal reveal-1 card-lift rounded-xl border border-accent/30 bg-ink-900/60 p-6">
            <div className="flex items-center gap-3">
              <span className="grid h-10 w-10 place-items-center rounded-lg bg-accent/15">
                <KeyRound className="h-5 w-5 text-accent" />
              </span>
              <h3 className="text-lg font-semibold">L2 · Capability Provenance</h3>
            </div>
            <p className="mt-3 leading-relaxed text-white/60">
              Every tool call must carry a signed token scoped to the real user request. An injected
              call — even a perfectly-worded one — has no token for that scope, so it is denied. The
              attack never gets authority to act.
            </p>
          </div>
          <div className="reveal reveal-2 card-lift rounded-xl border border-review/30 bg-ink-900/60 p-6">
            <div className="flex items-center gap-3">
              <span className="grid h-10 w-10 place-items-center rounded-lg bg-review/15">
                <Eye className="h-5 w-5 text-review" />
              </span>
              <h3 className="text-lg font-semibold">L3 · Canary Tripwires</h3>
            </div>
            <p className="mt-3 leading-relaxed text-white/60">
              Decoy secrets are seeded into the agent&apos;s context. They have no legitimate reason to
              leave the boundary. If one ever does, that is hard proof of exfiltration — zero false
              positives, by construction.
            </p>
          </div>
        </div>
        <p className="reveal mt-6 text-center text-sm text-white/45">
          These are the two layers an LLM firewall structurally cannot have. <span className="text-white/75">That&apos;s the moat.</span>
        </p>
      </section>

      {/* Agentic-era threats → TripWire's answer */}
      <Anchor id="threats" />
      <section className="mx-auto max-w-6xl px-6 py-14">
        <div className="reveal max-w-3xl">
          <span className="font-mono text-xs uppercase tracking-widest text-block">The agentic-era threat</span>
          <h2 className="mt-3 text-2xl font-bold sm:text-4xl">
            The moment an agent can <span className="grad-text">act</span>, your attack surface changes.
          </h2>
          <p className="mt-4 text-pretty leading-relaxed text-white/60">
            A chatbot that only talks has a small blast radius. An agent that reads your data, calls
            tools, spends money, and remembers — that&apos;s a new class of risk, and prompt filters
            don&apos;t cover it. Here is what actually goes wrong in production, and what TripWire does
            about each.
          </p>
        </div>

        <div className="mt-9 grid gap-4 lg:grid-cols-2">
          {THREATS.map((t, i) => (
            <div
              key={t.pain}
              className={`reveal reveal-${Math.min(i + 1, 5)} card-lift rounded-xl border border-ink-600 bg-ink-900/60 p-5`}
            >
              <div className="flex items-center gap-3">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-block/12">
                  <t.icon className="h-5 w-5 text-block" />
                </span>
                <h3 className="text-lg font-semibold">{t.pain}</h3>
              </div>
              <p className="mt-3 text-sm leading-relaxed text-white/55">{t.painBody}</p>
              <div className="mt-4 flex items-start gap-2 rounded-lg border border-allow/20 bg-allow/5 p-3">
                <ShieldCheck className="mt-0.5 h-4 w-4 shrink-0 text-allow" />
                <p className="text-sm leading-relaxed text-white/75">{t.answer}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="reveal mt-8 flex flex-col items-center gap-3 rounded-2xl border border-accent/30 bg-gradient-to-br from-ink-900 to-ink-800 p-7 text-center">
          <h3 className="text-xl font-bold sm:text-2xl">Which of these is your agent exposed to right now?</h3>
          <p className="max-w-xl text-white/60">
            Paste your agent&apos;s system prompt and get an instant security scorecard — free, no API
            key, 30 seconds. See exactly what gets through, and what TripWire blocks.
          </p>
          <Link
            href="/test-your-agent"
            className="mt-2 inline-flex items-center gap-2 rounded-lg bg-accent px-5 py-3 font-semibold text-ink-950 transition hover:bg-accent-glow"
          >
            <ShieldAlert className="h-4 w-4" /> Test your agent free <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>

      {/* How it works — architecture */}
      <Anchor id="how" />
      <section className="mx-auto max-w-6xl px-6 py-14">
        <h2 className="reveal text-2xl font-bold sm:text-3xl">How it works</h2>
        <p className="reveal mt-2 max-w-2xl text-white/55">
          TripWire sits inline between your agent and the world — across the three boundaries every
          agent exposes: the prompt, the tools/MCP, and the memory.
        </p>

        {/* flow */}
        <div className="reveal reveal-1 mt-8 flex flex-col items-stretch gap-3 sm:flex-row sm:items-center">
          {[
            { t: "User", s: "real request" },
            { t: "AI Agent", s: "any framework" },
          ].map((n) => (
            <FlowNode key={n.t} title={n.t} sub={n.s} />
          ))}
          <ArrowRight className="mx-auto h-5 w-5 shrink-0 rotate-90 text-accent sm:rotate-0" />
          <div className="card-lift flex-1 rounded-xl border-2 border-accent bg-ink-900 p-4 text-center shadow-glow">
            <ShieldHalf className="mx-auto h-6 w-6 text-accent" />
            <p className="mt-1 font-semibold">TripWire</p>
            <p className="text-xs text-white/45">L1–L5 inline · allow / review / block</p>
          </div>
          <ArrowRight className="mx-auto h-5 w-5 shrink-0 rotate-90 text-accent sm:rotate-0" />
          <FlowNode title="World" sub="tools · data · money" />
        </div>

        {/* Azure chips */}
        <p className="reveal mt-10 font-mono text-xs uppercase tracking-widest text-[#39c5cf]">Runs on Azure</p>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {AZURE.map((a, i) => (
            <div
              key={a.name}
              className={`reveal reveal-${Math.min(i + 1, 5)} card-lift flex items-start gap-3 rounded-xl border border-ink-600 bg-ink-900/60 p-4`}
            >
              <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-[#39c5cf]/12">
                <a.icon className="h-5 w-5 text-[#39c5cf]" />
              </span>
              <div>
                <p className="font-medium">{a.name}</p>
                <p className="mt-0.5 text-sm text-white/50">{a.sub}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 5 layers */}
      <section className="mx-auto max-w-6xl px-6 py-14">
        <h2 className="reveal mb-2 text-2xl font-bold sm:text-3xl">Defense in depth — 5 layers</h2>
        <p className="reveal mb-7 max-w-2xl text-sm text-white/50">
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

      {/* Business */}
      <Anchor id="business" />
      <section className="mx-auto max-w-6xl px-6 py-14">
        <h2 className="reveal text-2xl font-bold sm:text-3xl">Built to be a company</h2>
        <p className="reveal mt-2 max-w-2xl text-white/55">
          TripWire isn&apos;t a feature — it&apos;s the security, identity, and governance layer enterprises
          install before they let agents touch production systems.
        </p>

        <div className="mt-7 grid gap-4 lg:grid-cols-3">
          {BUSINESS.map((b, i) => (
            <div
              key={b.title}
              className={`reveal reveal-${Math.min(i + 1, 5)} card-lift rounded-xl border border-ink-600 bg-ink-900/60 p-6`}
            >
              <b.icon className="h-6 w-6 text-accent" />
              <h3 className="mt-3 text-lg font-semibold">{b.title}</h3>
              <p className="mt-2 leading-relaxed text-white/60">{b.body}</p>
            </div>
          ))}
        </div>

        <div className="reveal mt-4 grid gap-4 sm:grid-cols-3">
          {MARKET.map((m) => (
            <div key={m.v} className="rounded-xl border border-ink-600 bg-ink-800/40 p-5">
              <p className="grad-text font-mono text-xl font-bold">{m.k}</p>
              <p className="mt-1 text-sm text-white/55">{m.v}</p>
            </div>
          ))}
        </div>
        <p className="reveal mt-4 text-xs text-white/35">
          Market figures are top-down, directional. Full plan in the deck and BUSINESS_PLAN.md.
        </p>
      </section>

      {/* Roadmap */}
      <section className="mx-auto max-w-6xl px-6 py-14">
        <h2 className="reveal text-2xl font-bold sm:text-3xl">Where it&apos;s going</h2>
        <p className="reveal mt-2 max-w-2xl text-white/55">
          A control plane, not a single feature. The roadmap turns three primitives — provenance,
          taint/canary, and inline policy — into a full agent-security platform.
        </p>
        <div className="mt-7 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {ROADMAP.map((r, i) => (
            <div
              key={r.tag}
              className={`reveal reveal-${Math.min(i + 1, 5)} card-lift rounded-xl border border-ink-600 bg-ink-900/60 p-5`}
            >
              <div className="flex items-center gap-3">
                <span className="rounded-md bg-accent/15 px-2 py-1 font-mono text-xs font-bold text-accent">{r.tag}</span>
                <r.icon className="h-5 w-5 text-white/60" />
              </div>
              <h3 className="mt-3 font-medium">{r.name}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-white/55">{r.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* About */}
      <Anchor id="about" />
      <section className="mx-auto max-w-6xl px-6 py-14">
        <div className="grid gap-8 lg:grid-cols-[1.4fr_1fr]">
          <div className="reveal">
            <span className="font-mono text-xs uppercase tracking-widest text-accent">About the builder</span>
            <h2 className="mt-3 text-2xl font-bold sm:text-3xl">Kundan Khatri</h2>
            <p className="mt-1 text-white/60">Founder &amp; engineer — AI agent security · solo build</p>
            <div className="mt-5 space-y-4 leading-relaxed text-white/65">
              <p>
                I designed and built TripWire end-to-end — the architecture, the FastAPI defense engine,
                the cryptographic capability-provenance layer, the canary system, the live arena UI, the
                Azure infrastructure-as-code, and the honest benchmark harness. Solo.
              </p>
              <p>
                The thesis is simple and, I think, important: the industry is racing to give AI agents
                real power, but the security model still inspects <em>text</em>, not <em>actions</em>. I
                built the layer that governs what an agent is actually allowed to do — and proves nothing
                harmful left the boundary. The two ideas I&apos;m proudest of — denying injected calls
                their <em>authority</em> (provenance) and catching theft with <em>canaries</em> — stop the
                indirect-injection attacks a prompt firewall structurally can&apos;t.
              </p>
              <p>
                I care about shipping real systems on real infrastructure, and about being honest with
                numbers — TripWire reports its block rate <em>with</em> its false-positive rate, always.
                If you&apos;re building in agent security, AI safety, or applied infrastructure, I&apos;d
                love to talk.
              </p>
            </div>
            <div className="mt-6 flex flex-wrap gap-3">
              <a
                href="mailto:kundanlm10@gmail.com"
                className="inline-flex items-center gap-2 rounded-lg bg-accent px-4 py-2.5 font-semibold text-ink-950 transition hover:bg-accent-glow"
              >
                <Mail className="h-4 w-4" /> kundanlm10@gmail.com
              </a>
              <a
                href="https://github.com/KundanKhatri"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 rounded-lg border border-ink-600 px-4 py-2.5 font-semibold text-white/80 transition hover:text-white"
              >
                <Github className="h-4 w-4" /> github.com/KundanKhatri
              </a>
            </div>
          </div>

          <div className="reveal reveal-2 rounded-xl border border-ink-600 bg-ink-900/60 p-6">
            <h3 className="font-semibold">Shipped for this build</h3>
            <ul className="mt-4 space-y-3">
              {SHIPPED.map((s) => (
                <li key={s} className="flex items-start gap-2.5 text-sm text-white/65">
                  <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-allow" />
                  <span>{s}</span>
                </li>
              ))}
            </ul>
            <div className="mt-6 flex flex-wrap gap-2 text-xs">
              {["Python", "FastAPI", "Next.js", "TypeScript", "Azure", "pgvector", "Bicep", "Cryptography"].map((t) => (
                <span key={t} className="rounded-md border border-ink-600 bg-ink-800/50 px-2.5 py-1 font-mono text-white/55">
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="mx-auto max-w-6xl px-6 py-14">
        <div className="reveal overflow-hidden rounded-2xl border border-accent/30 bg-gradient-to-br from-ink-900 to-ink-800 p-8 text-center sm:p-12">
          <h2 className="text-2xl font-bold sm:text-4xl">Make it safe to give an agent power.</h2>
          <p className="mx-auto mt-3 max-w-xl text-white/60">
            It&apos;s live, the code is open, and you can attack it right now.
          </p>
          <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
            <a href="#arena" className="inline-flex items-center gap-2 rounded-lg bg-accent px-5 py-3 font-semibold text-ink-950 transition hover:bg-accent-glow">
              Attack the arena <ArrowRight className="h-4 w-4" />
            </a>
            <a href="/Tripwire/TripWire_Deck.pdf" className="inline-flex items-center gap-2 rounded-lg border border-ink-600 px-5 py-3 font-semibold text-white/80 transition hover:text-white">
              <FileText className="h-4 w-4" /> Download the deck
            </a>
            <a href="https://github.com/KundanKhatri/Tripwire" target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 rounded-lg border border-ink-600 px-5 py-3 font-semibold text-white/80 transition hover:text-white">
              <Github className="h-4 w-4" /> Star on GitHub
            </a>
          </div>
        </div>
      </section>

      <footer className="mx-auto max-w-6xl px-6 py-10 text-center text-xs text-white/30">
        TripWire · The control plane for AI agent actions · Built solo by Kundan Khatri for Microsoft
        Build AI 2026 · Azure OpenAI · Content Safety · Container Apps · Cosmos pgvector
      </footer>
    </main>
  );
}

function FlowNode({ title, sub }: { title: string; sub: string }) {
  return (
    <div className="card-lift flex-1 rounded-xl border border-ink-600 bg-ink-900/60 p-4 text-center">
      <p className="font-semibold">{title}</p>
      <p className="text-xs text-white/45">{sub}</p>
    </div>
  );
}
