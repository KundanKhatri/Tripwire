import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TripWire — Defense for Agentic AI",
  description:
    "A 5-layer prompt-injection and exfiltration defense for agentic systems, built on Azure. Attack it yourself.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        <div className="aurora" aria-hidden />
        <div className="grid-bg" aria-hidden />
        {children}
      </body>
    </html>
  );
}
