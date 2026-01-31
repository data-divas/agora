"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { DiscoverMap } from "./DiscoverMap";
import {
  DISCOVER_SITES,
  type DiscoverSite,
  type SiteStatus,
} from "./sample-data";

const STATUS_LABELS: Record<SiteStatus, string> = {
  seeking: "Seeking funding",
  funded: "Funded",
  "in-progress": "In development",
};

const STATUS_STYLES: Record<SiteStatus, string> = {
  seeking: "bg-agora-light/80 text-agora-dark",
  funded: "bg-agora-medium/80 text-white",
  "in-progress": "bg-agora-dark/90 text-white",
};

export default function DiscoverPage() {
  const [selectedSite, setSelectedSite] = useState<DiscoverSite | null>(
    DISCOVER_SITES[0]
  );
  const [activeTab, setActiveTab] = useState<SiteStatus | "all">("all");

  const filteredSites =
    activeTab === "all"
      ? DISCOVER_SITES
      : DISCOVER_SITES.filter((s) => s.status === activeTab);

  useEffect(() => {
    setSelectedSite((prev) => {
      if (!prev || !filteredSites.some((s) => s.id === prev.id)) {
        return filteredSites[0] ?? null;
      }
      return prev;
    });
  }, [activeTab]);

  return (
    <div className="flex h-screen bg-[#FAFAFA]">
      {/* Left sidebar nav */}
      <aside className="flex w-16 flex-col items-center border-r border-black/5 bg-white py-6">
        <Link
          href="/"
          className="mb-8 text-2xl font-semibold text-agora-dark"
          aria-label="Agora home"
        >
          A
        </Link>
        <nav className="flex flex-1 flex-col items-center gap-6">
          <Link
            href="/"
            className="rounded-lg p-2 text-[#9ca3af] hover:bg-agora-surface hover:text-agora-dark transition-colors"
            aria-label="Home"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </Link>
          <div
            className="rounded-lg bg-agora-light/40 p-2 text-agora-dark"
            aria-current="page"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <Link
            href="/discover"
            className="rounded-lg p-2 text-[#9ca3af] hover:bg-agora-surface hover:text-agora-dark transition-colors"
            aria-label="Discover"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </Link>
        </nav>
      </aside>

      {/* Main content: list + map */}
      <div className="flex flex-1 min-w-0">
        {/* Left panel - site list */}
        <div className="flex w-full max-w-md flex-col border-r border-black/5 bg-white">
          <div className="border-b border-black/5 p-4">
            <div className="flex items-center justify-between">
              <h1 className="text-xl font-semibold text-[#1a1a1a]">
                Discover projects
              </h1>
              <button
                type="button"
                className="rounded-lg p-2 text-[#6b7280] hover:bg-agora-surface hover:text-agora-dark transition-colors"
                aria-label="Search"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
            <div className="mt-4 flex gap-2">
              {(["all", "seeking", "funded", "in-progress"] as const).map(
                (tab) => (
                  <button
                    key={tab}
                    type="button"
                    onClick={() => setActiveTab(tab)}
                    className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                      activeTab === tab
                        ? "bg-agora-dark text-white"
                        : "bg-agora-surface/50 text-[#6b7280] hover:bg-agora-surface hover:text-[#1a1a1a]"
                    }`}
                  >
                    {tab === "all" ? "All" : STATUS_LABELS[tab]}
                  </button>
                )
              )}
            </div>
          </div>

          {/* Scrollable list */}
          <div className="flex-1 overflow-y-auto">
            {filteredSites.map((site) => (
              <button
                key={site.id}
                type="button"
                onClick={() => setSelectedSite(site)}
                className={`w-full border-b border-black/5 px-4 py-4 text-left transition-colors hover:bg-agora-surface/30 ${
                  selectedSite?.id === site.id ? "bg-agora-surface/50" : ""
                }`}
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-medium text-[#1a1a1a]">
                      {site.city} → {site.plannedUse}
                    </p>
                    <p className="mt-0.5 text-sm text-[#6b7280]">
                      Project #{site.id}
                    </p>
                  </div>
                  <span
                    className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_STYLES[site.status]}`}
                  >
                    {STATUS_LABELS[site.status]}
                  </span>
                </div>
              </button>
            ))}
          </div>

          {/* Selected site detail card */}
          {selectedSite && (
            <div className="border-t border-black/5 bg-white p-4">
              <div className="rounded-xl border border-black/5 bg-[#FAFAFA] p-4">
                <p className="font-medium text-[#1a1a1a]">
                  {selectedSite.city} → {selectedSite.plannedUse}
                </p>
                <p className="mt-1 text-sm text-[#6b7280]">
                  Project #{selectedSite.id}
                </p>
                <div className="mt-4 space-y-2 text-sm">
                  <p className="text-[#6b7280]">
                    <span className="font-medium text-[#1a1a1a]">Address:</span>{" "}
                    {selectedSite.address}
                  </p>
                  <p className="text-[#6b7280]">
                    <span className="font-medium text-[#1a1a1a]">Planned:</span>{" "}
                    {selectedSite.plannedUse}
                  </p>
                  <div className="flex gap-4 pt-2">
                    <span className="text-agora-dark font-medium">
                      {selectedSite.fundingPercent}% funded
                    </span>
                    <span className="text-[#6b7280]">
                      {selectedSite.investors} investors
                    </span>
                  </div>
                </div>
                <button
                  type="button"
                  className="mt-4 w-full rounded-lg bg-agora-medium py-2.5 text-sm font-medium text-white hover:bg-agora-dark transition-colors"
                >
                  View details
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Right panel - map */}
        <div className="relative flex-1 min-h-[400px]">
          <DiscoverMap
            sites={filteredSites}
            selectedSite={selectedSite}
            onSelectSite={setSelectedSite}
          />
          {/* Map overlay - selected site summary */}
          {selectedSite && (
            <div className="absolute bottom-4 left-4 right-4 rounded-xl border border-black/5 bg-white/95 px-4 py-3 shadow-lg backdrop-blur-sm md:left-auto md:right-4 md:w-80">
              <div className="flex items-center justify-between">
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_STYLES[selectedSite.status]}`}
                >
                  {STATUS_LABELS[selectedSite.status]}
                </span>
                <span className="text-sm text-[#6b7280]">
                  {selectedSite.fundingPercent}% · {selectedSite.investors} investors
                </span>
              </div>
              <p className="mt-2 font-medium text-[#1a1a1a]">
                {selectedSite.name}
              </p>
              <p className="text-sm text-[#6b7280]">
                {selectedSite.city} → {selectedSite.plannedUse}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
