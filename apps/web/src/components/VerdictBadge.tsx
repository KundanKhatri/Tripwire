import { cn } from "@/lib/cn";
import { Verdict } from "@/lib/types";
import { ShieldCheck, ShieldAlert, ShieldX } from "lucide-react";

const MAP = {
  allow: { label: "ALLOWED", cls: "text-allow border-allow/40 bg-allow/10", Icon: ShieldCheck },
  review: { label: "REVIEW", cls: "text-review border-review/40 bg-review/10", Icon: ShieldAlert },
  block: { label: "BLOCKED", cls: "text-block border-block/40 bg-block/10", Icon: ShieldX },
} as const;

export function VerdictBadge({ verdict, large }: { verdict: Verdict; large?: boolean }) {
  const { label, cls, Icon } = MAP[verdict];
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full border font-mono font-semibold tracking-wider",
        cls,
        large ? "px-4 py-2 text-sm" : "px-2.5 py-1 text-xs"
      )}
    >
      <Icon className={large ? "h-4 w-4" : "h-3.5 w-3.5"} />
      {label}
    </span>
  );
}
