export default function Steps() {
  const steps = [
    { t: "Create GitHub App", d: "Give it PR & contents permissions; add webhook URL from backend." },
    { t: "Deploy backend", d: "Use Railway. Copy the public webhook URL into your GitHub App." },
    { t: "Deploy this site", d: "Vercel → import /frontend, set links to your App’s installation URL." },
    { t: "Open a PR", d: "Bot posts a single consolidated review comment. Commit again to refresh." },
  ];
  return (
    <section className="container pb-16">
      <div className="grid gap-4 md:grid-cols-2">
        {steps.map((s,i)=>(
          <div key={i} className="card">
            <h3 className="text-xl font-semibold">{i+1}. {s.t}</h3>
            <p className="text-neutral-300 mt-2">{s.d}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
