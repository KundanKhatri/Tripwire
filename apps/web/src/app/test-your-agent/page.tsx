"use client";

import { useState } from "react";
import Link from "next/link";
import {
  ShieldHalf,
  ArrowLeft,
  Loader2,
  ShieldAlert,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  Mail,
} from "lucide-react";
import { assessAgent, submitLead, AssessResponse, Verdict } from "@/lib/assess";

const SAMPLE_PROMPT =
  "You are AcmeBot, a customer-support assistant for Acme Inc. You can read the knowledge base, look up orders, and send emails to customers. Be helpful and concise.";

const GRADE_COLOR: Record<string, string> = {
  A: "text-allow",
  B: "text-allow",
  C: "text-review",
  D: "text-review",
  F: "text-block",
};

const VERDICT_STYLE: Record<Verdict, { label: string; cls: string }> = {
  block: { label: "BLOCKED", cls: "text-block" },
  review: { label: "REVIEW", cls: "text-review" },
  allow: { label: "ALLOWED", cls: "text-white/50" },
};

export default function TestYourAgent() {
  const [name, setName] = useState("");
  const [prompt, setPrompt] = useState("");
  const [tools, setTools] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AssessResponse | null>(null);

  async function runAssessment() {
    if (!prompt.trim()) {
      setError("Paste your agent's system prompt to run the assessment.");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const data = await assessAgent({
        system_prompt: prompt.trim(),
        agent_name: name.trim() || "your agent",
        tools: tools.split(",").map((t) => t.trim()).filter(Boolean),
      });
      setResult(data);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch {
      setError("The assessment service is warming up. Give it a few seconds and try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="relative min-h-screen">
      <nav className="sticky top-0 z-40 border-b border-white/5 bg-ink-950/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3.5">
          <Link href="/" className="flex items-center gap-2">
            <ShieldHalf className="h-6 w-6 text-accent" />
            <span className="font-mono text-lg font-bold tracking-tight">TripWire</span>
          </Link>
          <Link href="/" className="flex items-center gap-1.5 text-sm text-white/55 transition hover:text-white">
            <ArrowLeft className="h-4 w-4" /> Back to home
          </Link>
        </div>
      </nav>

      <section className="mx-auto max-w-5xl px-6 pb-10 pt-14">
        {!result && (
          <div className="reveal mx-auto max-w-2xl text-center">
            <span className="inline-block rounded-full border border-accent/30 bg-accent/10 px-3 py-1 font-mono text-xs text-accent">
              Free · no API key · ~30 seconds
            </span>
            <h1 className="mt-6 text-balance text-4xl font-bold leading-tight tracking-tight sm:text-5xl">
              Is your AI agent <span className="grad-text">actually secure?</span>
            </h1>
            <p className="mx-auto mt-4 max-w-xl text-pretty text-lg text-white/60">
              Paste your agent&apos;s system prompt. We run a real prompt-injection, tool-poisoning,
              and data-exfiltration battery against its configuration — and show you exactly what
              gets through, and what TripWire blocks.
            </p>
          </div>
        )}

        {/* Intake form */}
        {!result && (
          <div className="reveal reveal-1 mx-auto mt-9 max-w-2xl rounded-2xl border border-ink-600 bg-ink-900/60 p-6 backdrop-blur">
            <label className="block text-sm font-medium text-white/70">Agent name (optional)</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="AcmeBot"
              className="mt-1.5 w-full rounded-lg border border-ink-600 bg-ink-950 px-3 py-2.5 text-sm text-white/90 outline-none placeholder:text-white/25 focus:border-accent/60"
            />
            <div className="mt-4 flex items-center justify-between">
              <label className="block text-sm font-medium text-white/70">Your agent&apos;s system prompt</label>
              <button
                onClick={() => { setName("AcmeBot"); setPrompt(SAMPLE_PROMPT); setTools("read_kb, lookup_order, send_email"); }}
                className="text-xs text-accent/80 transition hover:text-accent"
              >
                Use a sample
              </button>
            </div>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={7}
              placeholder="You are a helpful assistant that can read documents, look up data, and send emails…"
              className="mt-1.5 w-full resize-none rounded-lg border border-ink-600 bg-ink-950 p-3 font-mono text-sm leading-relaxed text-white/90 outline-none placeholder:text-white/25 focus:border-accent/60"
            />
            <label className="mt-4 block text-sm font-medium text-white/70">Tools it can call (optional, comma-separated)</label>
            <input
              value={tools}
              onChange={(e) => setTools(e.target.value)}
              placeholder="read_kb, lookup_order, send_email"
              className="mt-1.5 w-full rounded-lg border border-ink-600 bg-ink-950 px-3 py-2.5 font-mono text-sm text-white/90 outline-none placeholder:text-white/25 focus:border-accent/60"
            />

            {error && <p className="mt-3 text-sm text-block">{error}</p>}

            <button
              onClick={runAssessment}
              disabled={busy}
              className="glow-pulse mt-5 flex w-full items-center justify-center gap-2 rounded-lg bg-accent px-4 py-3 font-semibold text-ink-950 transition hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
            >
              {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <ShieldAlert className="h-4 w-4" />}
              {busy ? "Running attack battery…" : "Run the security assessment"}
            </button>
            <p className="mt-3 text-center text-xs text-white/35">
              We never call your model and store nothing. Your prompt is analyzed and a real attack
              battery is run through TripWire&apos;s live pipeline on Azure.
            </p>
          </div>
        )}

        {/* Scorecard */}
        {result && <Scorecard result={result} onReset={() => { setResult(null); setError(null); }} />}
      </section>
    </main>
  );
}

function Scorecard({ result, onReset }: { result: AssessResponse; onReset: () => void }) {
  return (
    <div className="reveal mx-auto max-w-3xl">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold sm:text-3xl">
          Security scorecard — <span className="text-white/70">{result.agent_name}</span>
        </h1>
        <button onClick={onReset} className="text-sm text-white/50 transition hover:text-white">
          Test another
        </button>
      </div>

      {/* Grade comparison */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className="card-lift rounded-2xl border border-block/30 bg-ink-900/60 p-6 text-center">
          <p className="text-xs font-medium uppercase tracking-widest text-white/45">Without TripWire</p>
          <p className={`mt-2 font-mono text-7xl font-bold ${GRADE_COLOR[result.exposure_grade] || "text-block"}`}>
            {result.exposure_grade}
          </p>
          <p className="mt-2 text-sm text-white/60">
            Exposed to <span className="font-semibold text-block">{result.exposed_count}</span> of {result.total_attacks} attacks
          </p>
        </div>
        <div className="card-lift rounded-2xl border border-allow/30 bg-ink-900/60 p-6 text-center">
          <p className="text-xs font-medium uppercase tracking-widest text-white/45">With TripWire</p>
          <p className={`mt-2 font-mono text-7xl font-bold ${GRADE_COLOR[result.protected_grade] || "text-allow"}`}>
            {result.protected_grade}
          </p>
          <p className="mt-2 text-sm text-white/60">
            Caught <span className="font-semibold text-allow">{result.tripwire_caught}</span> of {result.total_attacks} attacks
          </p>
        </div>
      </div>

      <p className="mt-5 rounded-xl border border-ink-600 bg-ink-800/40 p-4 text-sm leading-relaxed text-white/75">
        {result.summary}
      </p>

      {/* Attack table */}
      <h2 className="mt-8 text-lg font-semibold">Attack-by-attack</h2>
      <div className="mt-3 overflow-hidden rounded-xl border border-ink-600">
        <table className="w-full text-left text-sm">
          <thead className="bg-ink-800/60 text-xs uppercase tracking-wider text-white/45">
            <tr>
              <th className="px-4 py-2.5 font-medium">Attack</th>
              <th className="px-4 py-2.5 font-medium">Your agent</th>
              <th className="px-4 py-2.5 font-medium">TripWire</th>
            </tr>
          </thead>
          <tbody>
            {result.attacks.map((a, i) => {
              const v = VERDICT_STYLE[a.tripwire_verdict];
              return (
                <tr key={i} className="border-t border-ink-700/60">
                  <td className="px-4 py-3">
                    <div className="font-medium text-white/85">{a.attack_type}</div>
                    <span className={`mt-0.5 inline-block rounded px-1.5 py-0.5 text-[10px] uppercase tracking-wide ${a.attack_class === "action" ? "bg-[#b57bff]/15 text-[#b57bff]" : "bg-white/10 text-white/45"}`}>
                      {a.attack_class === "action" ? "action-layer" : "prompt-layer"}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    {a.agent_exposed ? (
                      <span className="inline-flex items-center gap-1.5 text-block"><XCircle className="h-4 w-4" /> exposed</span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 text-allow"><CheckCircle2 className="h-4 w-4" /> defended</span>
                    )}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center gap-1.5 font-medium ${v.cls}`}>
                      <ShieldCheck className="h-4 w-4" /> {v.label}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Weaknesses / strengths */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl border border-ink-600 bg-ink-900/60 p-5">
          <h3 className="flex items-center gap-2 font-semibold text-block"><AlertTriangle className="h-4 w-4" /> Gaps in your prompt</h3>
          <ul className="mt-3 space-y-2">
            {result.weaknesses.length === 0 && <li className="text-sm text-white/50">No prompt-level gaps detected.</li>}
            {result.weaknesses.map((w) => (
              <li key={w} className="flex items-start gap-2 text-sm text-white/65"><XCircle className="mt-0.5 h-4 w-4 shrink-0 text-block/80" />{w}</li>
            ))}
          </ul>
        </div>
        <div className="rounded-xl border border-ink-600 bg-ink-900/60 p-5">
          <h3 className="flex items-center gap-2 font-semibold text-allow"><CheckCircle2 className="h-4 w-4" /> What your prompt does well</h3>
          <ul className="mt-3 space-y-2">
            {result.strengths.length === 0 && <li className="text-sm text-white/50">No explicit guardrails found in the prompt.</li>}
            {result.strengths.map((s) => (
              <li key={s} className="flex items-start gap-2 text-sm text-white/65"><CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-allow/80" />{s}</li>
            ))}
          </ul>
        </div>
      </div>

      <p className="mt-5 rounded-xl border border-[#b57bff]/25 bg-[#b57bff]/5 p-4 text-sm leading-relaxed text-white/70">
        <span className="font-semibold text-[#b57bff]">The honest part:</span> the <span className="font-medium">action-layer</span> attacks
        (indirect injection, tool & data exfiltration) cannot be fixed by any system prompt — a model
        can always be talked into trying them. They need provenance and canaries at the action layer.
        That is exactly the gap TripWire closes.
      </p>

      <LeadForm grade={result.exposure_grade} agentName={result.agent_name} />
    </div>
  );
}

function LeadForm({ grade, agentName }: { grade: string; agentName: string }) {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [website, setWebsite] = useState(""); // honeypot
  const [state, setState] = useState<"idle" | "sending" | "done" | "error">("idle");
  const [err, setErr] = useState<string | null>(null);

  async function send() {
    setState("sending");
    setErr(null);
    const res = await submitLead({ email, message, grade, agent_context: agentName, website });
    if (res.ok) setState("done");
    else { setState("error"); setErr(res.error || "Something went wrong."); }
  }

  if (state === "done") {
    return (
      <div className="mt-8 rounded-2xl border border-allow/30 bg-allow/5 p-6 text-center">
        <CheckCircle2 className="mx-auto h-8 w-8 text-allow" />
        <h3 className="mt-3 text-lg font-semibold">You&apos;re on the list.</h3>
        <p className="mt-1 text-sm text-white/60">I&apos;ll reach out with a full security review of {agentName}. — Kundan</p>
      </div>
    );
  }

  return (
    <div className="mt-8 overflow-hidden rounded-2xl border border-accent/30 bg-gradient-to-br from-ink-900 to-ink-800 p-6 sm:p-8">
      <h3 className="text-xl font-bold sm:text-2xl">Want the full picture?</h3>
      <p className="mt-2 text-white/60">
        This was a 10-attack sample. Get a complete security review of your agent — the full corpus,
        your real tool graph, and a hardening plan. Free for early teams.
      </p>
      {/* Honeypot — hidden from users, bots fill it and get silently dropped */}
      <input
        type="text"
        name="website"
        tabIndex={-1}
        autoComplete="off"
        aria-hidden="true"
        value={website}
        onChange={(e) => setWebsite(e.target.value)}
        className="absolute left-[-9999px] h-0 w-0 opacity-0"
      />
      <div className="mt-5 flex flex-col gap-3 sm:flex-row">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@company.com"
          className="flex-1 rounded-lg border border-ink-600 bg-ink-950 px-3 py-2.5 text-sm text-white/90 outline-none placeholder:text-white/25 focus:border-accent/60"
        />
        <button
          onClick={send}
          disabled={state === "sending" || !email}
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-accent px-5 py-2.5 font-semibold text-ink-950 transition hover:bg-accent-glow disabled:cursor-not-allowed disabled:opacity-50"
        >
          {state === "sending" ? <Loader2 className="h-4 w-4 animate-spin" /> : <Mail className="h-4 w-4" />}
          Book a security review
        </button>
      </div>
      <textarea
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        rows={2}
        placeholder="Anything about your agent or stack? (optional)"
        className="mt-3 w-full resize-none rounded-lg border border-ink-600 bg-ink-950 p-3 text-sm text-white/90 outline-none placeholder:text-white/25 focus:border-accent/60"
      />
      {err && <p className="mt-2 text-sm text-block">{err}</p>}
      <p className="mt-3 text-xs text-white/35">Or email <a href="mailto:kundanlm10@gmail.com" className="text-accent/80 hover:text-accent">kundanlm10@gmail.com</a> directly.</p>
    </div>
  );
}
