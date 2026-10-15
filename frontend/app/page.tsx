"use client";

import { useState } from "react";

// The same shape the Python judge returns. This is the contract between
// the frontend and the backend, so keep it in sync with graph/state.py.
type Verdict = {
  verdict: "SCAM" | "SUSPICIOUS" | "UNSURE" | "SAFE";
  risk: number;
  scam_type: string | null;
  reasons: string[];
  sources: string[];
};

const LOOK = {
  SCAM: {
    title: "This looks like a scam",
    bar: "bg-[#B3261E]",
    text: "text-[#B3261E]",
    advice: "Don't click any links, reply, or send money or codes. Block and delete it.",
  },
  SUSPICIOUS: {
    title: "This looks suspicious",
    bar: "bg-[#A15C00]",
    text: "text-[#A15C00]",
    advice: "Don't click links. Contact the person or company using a number or website you already trust.",
  },
  UNSURE: {
    title: "We can't confirm this is safe",
    bar: "bg-[#4A5568]",
    text: "text-[#4A5568]",
    advice: "Check through the official website or app before doing anything.",
  },
  SAFE: {
    title: "This looks safe",
    bar: "bg-[#2E7D4F]",
    text: "text-[#2E7D4F]",
    advice: "Still, never share passwords or one-time codes with anyone.",
  },
};

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// Sends the message to the FastAPI server, which runs the real investigation.
async function checkMessage(message: string): Promise<Verdict> {
  const res = await fetch(`${API_URL}/check`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error(`Server returned ${res.status}`);
  return res.json();
}

export default function Home() {
  const [message, setMessage] = useState("");
  const [result, setResult] = useState<Verdict | null>(null);
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState("");

  async function handleCheck() {
    if (!message.trim()) {
      setError("Paste a message first, then press Check message.");
      return;
    }
    setError("");
    setResult(null);
    setChecking(true);
    try {
      setResult(await checkMessage(message));
    } catch {
      setError("The check didn't finish. Try again in a moment.");
    } finally {
      setChecking(false);
    }
  }

  const look = result ? LOOK[result.verdict] : null;

  return (
    <main className="min-h-screen bg-[#EEF3F8] px-5 py-12 text-[#1F2A44] sm:py-20">
      <div className="mx-auto max-w-2xl">
        <p className="text-lg font-bold">Scam Guardian</p>

        <h1 className="mt-6 text-4xl font-bold leading-tight sm:text-5xl">
          Got a message that feels off?
        </h1>
        <p className="mt-4 text-xl leading-relaxed">
          Paste it below. We&apos;ll check the links, the sender and the wording, and tell you what to do.
        </p>

        <label htmlFor="message" className="mt-10 block text-lg font-bold">
          The message
        </label>
        <textarea
          id="message"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          rows={6}
          placeholder="For example: USPS: Your package is on hold. Pay $1.99 at..."
          className="mt-2 w-full rounded-lg border-2 border-[#1F2A44]/30 bg-white p-4 text-lg leading-relaxed focus:border-[#1F2A44] focus:outline-none focus-visible:ring-4 focus-visible:ring-[#1F2A44]/20"
        />

        <button
          onClick={handleCheck}
          disabled={checking}
          className="mt-4 w-full rounded-lg bg-[#1F2A44] px-8 py-4 text-xl font-bold text-white hover:bg-[#2C3A5C] focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-[#1F2A44]/30 disabled:opacity-60 sm:w-auto"
        >
          {checking ? "Checking…" : "Check message"}
        </button>

        {error && (
          <p role="alert" className="mt-4 text-lg font-bold text-[#B3261E]">
            {error}
          </p>
        )}

        <div aria-live="polite">
          {result && look && (
            <section className="mt-10 flex overflow-hidden rounded-lg bg-white">
              <div className={`w-3 shrink-0 ${look.bar}`} />
              <div className="p-6">
                <h2 className={`text-3xl font-bold ${look.text}`}>{look.title}</h2>
                <p className="mt-1 text-lg">
                  Risk {result.risk} out of 100
                  {result.scam_type ? `, ${result.scam_type}` : ""}
                </p>

                <ul className="mt-5 list-disc space-y-2 pl-5 text-lg leading-relaxed">
                  {result.reasons.map((reason) => (
                    <li key={reason}>{reason}</li>
                  ))}
                </ul>

                <h3 className="mt-6 text-lg font-bold">What to do</h3>
                <p className="mt-1 text-lg leading-relaxed">{look.advice}</p>

                {result.sources.length > 0 && (
                  <>
                    <h3 className="mt-6 text-lg font-bold">Where we checked</h3>
                    <ul className="mt-1 space-y-1 text-lg">
                      {result.sources.map((url) => (
                        <li key={url}>
                          <a href={url} target="_blank" rel="noreferrer" className="break-all underline">
                            {url}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            </section>
          )}
        </div>
      </div>
    </main>
  );
}
