export type HealthStatus = {
  status: string;
};

const defaultApiBaseUrl =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export async function fetchBackendHealth(
  apiBaseUrl: string = defaultApiBaseUrl,
): Promise<HealthStatus> {
  const trimmedBaseUrl = apiBaseUrl.replace(/\/$/, "");
  const response = await fetch(`${trimmedBaseUrl}/health`);

  if (!response.ok) {
    throw new Error("Failed to fetch backend health status");
  }

  return (await response.json()) as HealthStatus;
}
