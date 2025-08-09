export default function Setup() {
  return (
    <section className="container py-16">
      <div className="card">
        <h1 className="text-3xl font-bold">Setup</h1>
        <ol className="list-decimal ml-6 mt-4 space-y-2 text-neutral-300">
          <li>Deploy the backend (Railway). Copy the public <b>/webhook</b> URL.</li>
          <li>Create a GitHub App (Developer settings → GitHub Apps). Use the webhook URL.</li>
          <li>Grant permissions: <b>Pull requests: Read & write</b>, <b>Contents: Read</b>, <b>Metadata: Read</b>.</li>
          <li>Subscribe to events: <b>Pull request</b>.</li>
          <li>Generate private key → base64 encode → save in backend env.</li>
          <li>Install the App on your repo(s). Open a PR to see the bot in action.</li>
        </ol>
      </div>
    </section>
  );
}
