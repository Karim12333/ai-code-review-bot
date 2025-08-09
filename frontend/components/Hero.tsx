'use client';

import { useState, useEffect } from 'react';

export default function Hero() {
  const [backendStatus, setBackendStatus] = useState<string>('checking...');
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://ai-code-review-bot-backend.vercel.app';

  useEffect(() => {
    fetch(`${apiUrl}/health`)
      .then(res => res.json())
      .then(data => setBackendStatus(data.ok ? '✅ Backend Online' : '❌ Backend Error'))
      .catch(() => setBackendStatus('❌ Backend Offline'));
  }, [apiUrl]);

  return (
    <section className="container py-16">
      <div className="card">
        <h1 className="text-4xl font-bold">AI Code Review Bot</h1>
        <p className="mt-3 text-neutral-300">
          Automatic pull-request reviews powered by GPT-4o. Faster feedback, fewer regressions.
        </p>
        <div className="mt-4 p-3 bg-neutral-800 rounded-lg">
          <span className="text-sm text-neutral-400">Backend Status: </span>
          <span className="text-sm font-mono">{backendStatus}</span>
        </div>
        <div className="mt-6 flex gap-3">
          <a className="btn" href="/setup">Install the GitHub App</a>
          <a className="btn" href={`${apiUrl}`} target="_blank" rel="noopener noreferrer">Test Backend API</a>
        </div>
      </div>
    </section>
  );
}
