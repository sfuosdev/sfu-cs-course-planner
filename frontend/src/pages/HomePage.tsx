import { StatusIndicator } from "../components/StatusIndicator";

export function HomePage() {
  return (
    <section>
      <p>
        A collaborative starter platform for SFU Computing Science students to
        plan courses, verify prerequisites, and track degree progress.
      </p>
      <StatusIndicator />
    </section>
  );
}
