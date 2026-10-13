import { useEffect, useState } from "react";

import { fetchBackendHealth } from "../services/health";

type StatusState = "loading" | "online" | "offline";

export function StatusIndicator() {
  const [status, setStatus] = useState<StatusState>("loading");

  useEffect(() => {
    let isMounted = true;

    const loadStatus = async () => {
      try {
        const result = await fetchBackendHealth();

        if (isMounted) {
          setStatus(result.status === "ok" ? "online" : "offline");
        }
      } catch {
        if (isMounted) {
          setStatus("offline");
        }
      }
    };

    void loadStatus();

    return () => {
      isMounted = false;
    };
  }, []);

  const label =
    status === "loading"
      ? "Checking backend status..."
      : status === "online"
        ? "Backend status: online"
        : "Backend status: offline";

  return <p>{label}</p>;
}
