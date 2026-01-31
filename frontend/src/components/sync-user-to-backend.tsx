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
        console.log("Got Privy token:", token ? "present" : "missing");
        if (!token) return;
        const res = await fetch(`${API_URL}/api/users/me`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        console.log("Backend /me response:", res.status, res.statusText);
        if (!res.ok) {
          const error = await res.text();
          console.error("Backend /me error:", error);
        } else {
          syncedRef.current = true;
          console.log("User synced to backend successfully");
        }
      } catch (error) {
        console.error("Failed to sync user to backend:", error);
      }
    };

    sync();
  }, [ready, authenticated, getAccessToken]);

  return null;
}
