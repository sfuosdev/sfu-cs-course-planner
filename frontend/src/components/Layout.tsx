import type { PropsWithChildren } from "react";

type LayoutProps = PropsWithChildren<{
  title: string;
}>;

export function Layout({ title, children }: LayoutProps) {
  return (
    <main style={{ margin: "0 auto", maxWidth: 720, padding: "2rem 1rem" }}>
      <header style={{ marginBottom: "1.5rem" }}>
        <h1>{title}</h1>
      </header>
      {children}
    </main>
  );
}
