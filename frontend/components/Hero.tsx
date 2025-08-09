export default function Hero() {
  return (
    <section className="container py-16">
      <div className="card">
        <h1 className="text-4xl font-bold">AI Code Review Bot</h1>
        <p className="mt-3 text-neutral-300">
          Automatic pull-request reviews powered by GPT-4o. Faster feedback, fewer regressions.
        </p>
        <div className="mt-6 flex gap-3">
          <a className="btn" href="/setup">Install the GitHub App</a>
          <a className="btn" href="https://github.com/new">Try on a sample repo</a>
        </div>
      </div>
    </section>
  );
}
