import Hero from "../components/Hero";
import Steps from "../components/Steps";

export default function Page() {
  return (
    <>
      <Hero />
      <Steps />
      <section className="container pb-24">
        <div className="card">
          <h2 className="text-2xl font-bold">Why teams use this</h2>
          <ul className="list-disc ml-6 mt-3 space-y-2 text-neutral-300">
            <li>Surface risky changes early (security/perf/correctness).</li>
            <li>Standardize style without human back-and-forth.</li>
            <li>Lightweight, configurable via <code>.aicodereview.yml</code>.</li>
          </ul>
        </div>
      </section>
    </>
  );
}
