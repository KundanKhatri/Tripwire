import type { Metadata } from "next";

const SITE = "https://kundankhatri.github.io/Tripwire";

export const metadata: Metadata = {
  title: "Test Your Agent — Free AI Agent Security Assessment",
  description:
    "Paste your AI agent's system prompt and get an instant security scorecard. See which prompt-injection, tool-poisoning, and data-exfiltration attacks your agent is exposed to — and how TripWire blocks them. Free, no API key, 30 seconds.",
  alternates: { canonical: `${SITE}/test-your-agent` },
  openGraph: {
    type: "website",
    url: `${SITE}/test-your-agent`,
    title: "Is your AI agent secure? Free 30-second assessment",
    description:
      "Run a real prompt-injection battery against your agent's configuration and get an exposure grade. See what TripWire blocks.",
    images: [{ url: `${SITE}/og.png`, width: 1200, height: 630 }],
  },
};

export default function TestLayout({ children }: { children: React.ReactNode }) {
  return children;
}
