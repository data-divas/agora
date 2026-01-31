"use client";

import { usePrivy } from "@privy-io/react-auth";

function truncate(str: string, len: number) {
  if (str.length <= len) return str;
  return `${str.slice(0, len)}…`;
}

export function AuthNav() {
  const { ready, authenticated, user, login, logout } = usePrivy();

  if (!ready) {
    return (
      <span className="rounded-full border border-white/20 px-4 py-2 text-sm text-[#9ca3af]">
        …
      </span>
    );
  }

  if (!authenticated || !user) {
    return (
      <button
        type="button"
        onClick={login}
        className="rounded-full bg-[#e8a838] px-4 py-2 text-sm font-medium text-[#0f1419] hover:bg-[#c4902a] transition-colors"
      >
        Get started
      </button>
    );
  }

  const label =
    user.wallet?.address != null
      ? truncate(user.wallet.address, 8)
      : user.email?.address ?? user.id ?? "Account";

  return (
    <div className="flex items-center gap-3">
      <span className="text-sm text-[#9ca3af]">{truncate(label, 16)}</span>
      <button
        type="button"
        onClick={logout}
        className="rounded-full border border-white/20 px-4 py-2 text-sm font-medium hover:border-white/40 hover:bg-white/5 transition-colors"
      >
        Log out
      </button>
    </div>
  );
}
