import type { Metadata } from "next";
import "./globals.css";

const SITE = "https://kundankhatri.github.io/Tripwire";

export const metadata: Metadata = {
  metadataBase: new URL(SITE),
  title: {
    default: "TripWire — The Control Plane for AI Agent Actions",
    template: "%s · TripWire",
  },
  description:
    "TripWire is the runtime security, identity, and governance layer for AI agents. A 5-layer defense — semantic firewall, capability provenance, canary tripwires, behavioral anomaly, learning classifier — that stops prompt injection, tool poisoning, and data exfiltration the attacks an LLM firewall can't. Built on Azure by Kundan Khatri for Microsoft Build AI 2026. Attack it yourself in the live arena.",
  applicationName: "TripWire",
  authors: [{ name: "Kundan Khatri", url: "https://github.com/KundanKhatri" }],
  creator: "Kundan Khatri",
  publisher: "Kundan Khatri",
  keywords: [
    "AI agent security",
    "prompt injection defense",
    "indirect prompt injection",
    "agentic AI security",
    "LLM firewall",
    "tool poisoning",
    "MCP security",
    "data exfiltration prevention",
    "capability provenance",
    "canary tokens",
    "Azure AI security",
    "Azure Prompt Shields",
    "AI governance",
    "agent control plane",
    "Microsoft Build AI 2026",
    "Kundan Khatri",
  ],
  alternates: { canonical: SITE },
  openGraph: {
    type: "website",
    url: SITE,
    siteName: "TripWire",
    title: "TripWire — The Control Plane for AI Agent Actions",
    description:
      "Stop prompt injection, tool poisoning, and data exfiltration at the action layer. A 5-layer agent defense built on Azure. Attack it yourself in the live arena.",
    images: [{ url: `${SITE}/og.png`, width: 1200, height: 630, alt: "TripWire — the control plane for AI agent actions" }],
  },
  twitter: {
    card: "summary_large_image",
    title: "TripWire — The Control Plane for AI Agent Actions",
    description:
      "A 5-layer defense that stops the agent attacks an LLM firewall can't. Built on Azure. Attack it yourself.",
    images: [`${SITE}/og.png`],
    creator: "@KundanKhatri",
  },
  icons: { icon: "/icon.svg", shortcut: "/icon.svg", apple: "/icon.svg" },
  category: "technology",
  robots: { index: true, follow: true },
};

const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "SoftwareApplication",
      name: "TripWire",
      applicationCategory: "SecurityApplication",
      operatingSystem: "Cloud / Azure",
      description:
        "A 5-layer runtime defense for AI agents: semantic firewall, capability provenance, canary tripwires, behavioral anomaly, and a learning classifier. Stops prompt injection, tool poisoning, and data exfiltration.",
      url: SITE,
      author: { "@type": "Person", name: "Kundan Khatri" },
      offers: { "@type": "Offer", price: "0", priceCurrency: "USD", description: "Open-core" },
    },
    {
      "@type": "Person",
      name: "Kundan Khatri",
      url: "https://github.com/KundanKhatri",
      email: "kundanlm10@gmail.com",
      jobTitle: "Founder & Engineer — AI agent security",
      knowsAbout: [
        "AI agent security",
        "prompt injection",
        "Azure AI",
        "FastAPI",
        "Next.js",
        "applied cryptography",
        "full-stack engineering",
      ],
      sameAs: ["https://github.com/KundanKhatri", "https://kundankhatri.github.io/Tripwire"],
    },
    {
      "@type": "WebSite",
      name: "TripWire",
      url: SITE,
      author: { "@type": "Person", name: "Kundan Khatri" },
    },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="font-sans antialiased">
        <div className="aurora" aria-hidden />
        <div className="grid-bg" aria-hidden />
        {children}
      </body>
    </html>
  );
}
