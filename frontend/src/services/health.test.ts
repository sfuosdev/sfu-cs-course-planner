import { afterEach, describe, expect, it, vi } from "vitest";

import { fetchBackendHealth } from "./health";

describe("fetchBackendHealth", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("requests /health and returns parsed JSON", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: "ok" }),
    });

    vi.stubGlobal("fetch", fetchMock);

    const result = await fetchBackendHealth("http://localhost:8000");

    expect(fetchMock).toHaveBeenCalledWith("http://localhost:8000/health");
    expect(result).toEqual({ status: "ok" });
  });
});
