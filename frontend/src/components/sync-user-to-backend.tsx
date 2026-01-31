"use client";

import { usePrivy } from "@privy-io/react-auth";
import { useEffect, useRef } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

/**
 * When the user is authenticated with Privy, call the backend GET /api/users/me
 * with the Bearer token so the backend can create/link the user in the DB (get_or_create by Privy DID).
 * Renders nothing.
 */
export function SyncUserToBackend() {
  const { ready, authenticated, getAccessToken } = usePrivy();
  const syncedRef = useRef(false);

  useEffect(() => {
    if (!ready || !authenticated) {
      syncedRef.current = false;
      return;
    }
    if (syncedRef.current) return;

    const sync = async () => {
      try {
        const token = await getAccessToken();
        if (!token) return;
        const res = await fetch(`${API_URL}/api/users/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok) syncedRef.current = true;
      } catch {
        // Retry on next mount or when effect re-runs
      }
    };

    sync();
  }, [ready, authenticated, getAccessToken]);

  return null;
}
