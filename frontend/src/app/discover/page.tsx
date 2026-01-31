"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { DiscoverMap } from "./DiscoverMap";
import { fetchParkingLots } from "./api";
import type { ParkingLot } from "./types";

export type ParkingFilter = "all" | "available" | "underutilized";

const FILTER_LABELS: Record<ParkingFilter, string> = {
  all: "All",
  available: "Available for rent",
  underutilized: "Underutilized",
};

export default function DiscoverPage() {
  const [parkingLots, setParkingLots] = useState<ParkingLot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLot, setSelectedLot] = useState<ParkingLot | null>(null);
  const [activeFilter, setActiveFilter] = useState<ParkingFilter>("all");

  useEffect(() => {
    fetchParkingLots()
      .then(setParkingLots)
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load"))
      .finally(() => setLoading(false));
  }, []);

  const filteredLots =
    activeFilter === "all"
      ? parkingLots
      : activeFilter === "available"
        ? parkingLots.filter((p) => p.is_available_for_rent === true)
        : parkingLots.filter(
            (p) =>
              (p.avg_utilization != null && p.avg_utilization < 40) ||
              (p.underutilized_hours != null && p.underutilized_hours > 0)
          );

  useEffect(() => {
    setSelectedLot((prev) => {
      if (!prev || !filteredLots.some((p) => p.id === prev.id)) {
        return filteredLots[0] ?? null;
      }
      return prev;
    });
  }, [activeFilter, filteredLots]);

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
        {/* Left panel - parking lot list */}
        <div className="flex w-full max-w-md flex-col border-r border-black/5 bg-white">
          <div className="border-b border-black/5 p-4">
            <div className="flex items-center justify-between">
              <h1 className="text-xl font-semibold text-[#1a1a1a]">
                Discover parking lots
              </h1>
            </div>
            <div className="mt-4 flex gap-2">
              {(["all", "available", "underutilized"] as const).map((tab) => (
                <button
                  key={tab}
                  type="button"
                  onClick={() => setActiveFilter(tab)}
                  className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                    activeFilter === tab
                      ? "bg-agora-dark text-white"
                      : "bg-agora-surface/50 text-[#6b7280] hover:bg-agora-surface hover:text-[#1a1a1a]"
                  }`}
                >
                  {FILTER_LABELS[tab]}
                </button>
              ))}
            </div>
          </div>

          {/* Scrollable list */}
          <div className="flex-1 overflow-y-auto">
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="h-8 w-8 animate-spin rounded-full border-2 border-agora-medium border-t-transparent" />
              </div>
            ) : error ? (
              <div className="p-4 text-sm text-red-600">{error}</div>
            ) : filteredLots.length === 0 ? (
              <div className="p-4 text-sm text-[#6b7280]">
                No parking lots found.
              </div>
            ) : (
              filteredLots.map((lot) => (
                <button
                  key={lot.id}
                  type="button"
                  onClick={() => setSelectedLot(lot)}
                  className={`w-full border-b border-black/5 px-4 py-4 text-left transition-colors hover:bg-agora-surface/30 ${
                    selectedLot?.id === lot.id ? "bg-agora-surface/50" : ""
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <p className="font-medium text-[#1a1a1a]">{lot.name}</p>
                      <p className="mt-0.5 text-sm text-[#6b7280] line-clamp-1">
                        {lot.address}
                      </p>
                      <div className="mt-1 flex gap-3 text-xs text-[#6b7280]">
                        {lot.avg_utilization != null && (
                          <span>{Math.round(lot.avg_utilization)}% avg use</span>
                        )}
                        {lot.estimated_capacity != null && (
                          <span>{lot.estimated_capacity} spots</span>
                        )}
                      </div>
                    </div>
                    {lot.is_available_for_rent && (
                      <span className="shrink-0 rounded-full bg-agora-light/80 px-2 py-0.5 text-xs font-medium text-agora-dark">
                        Available
                      </span>
                    )}
                  </div>
                </button>
              ))
            )}
          </div>

          {/* Selected lot detail card */}
          {selectedLot && (
            <div className="border-t border-black/5 bg-white p-4">
              <div className="rounded-xl border border-black/5 bg-[#FAFAFA] p-4">
                <p className="font-medium text-[#1a1a1a]">{selectedLot.name}</p>
                <p className="mt-1 text-sm text-[#6b7280] line-clamp-2">
                  {selectedLot.address}
                </p>
                <div className="mt-4 space-y-2 text-sm">
                  {selectedLot.avg_utilization != null && (
                    <p className="text-[#6b7280]">
                      <span className="font-medium text-[#1a1a1a]">Avg utilization:</span>{" "}
                      {Math.round(selectedLot.avg_utilization)}%
                    </p>
                  )}
                  {selectedLot.estimated_capacity != null && (
                    <p className="text-[#6b7280]">
                      <span className="font-medium text-[#1a1a1a]">Capacity:</span>{" "}
                      {selectedLot.estimated_capacity} spots
                    </p>
                  )}
                  {selectedLot.rating != null && (
                    <p className="text-[#6b7280]">
                      <span className="font-medium text-[#1a1a1a]">Rating:</span>{" "}
                      {selectedLot.rating}
                      {selectedLot.user_ratings_total != null &&
                        ` (${selectedLot.user_ratings_total} reviews)`}
                    </p>
                  )}
                  {selectedLot.contact_notes && (
                    <p className="text-[#6b7280]">
                      <span className="font-medium text-[#1a1a1a]">Notes:</span>{" "}
                      {selectedLot.contact_notes}
                    </p>
                  )}
                  {selectedLot.is_available_for_rent && (
                    <span className="inline-block rounded-full bg-agora-medium/90 px-2 py-0.5 text-xs font-medium text-white">
                      Available for rent
                    </span>
                  )}
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
            lots={filteredLots}
            selectedLot={selectedLot}
            onSelectLot={setSelectedLot}
          />
          {/* Map overlay - selected lot summary */}
          {selectedLot && (
            <div className="absolute bottom-4 left-4 right-4 rounded-xl border border-black/5 bg-white/95 px-4 py-3 shadow-lg backdrop-blur-sm md:left-auto md:right-4 md:w-80">
              <div className="flex items-center justify-between">
                {selectedLot.is_available_for_rent && (
                  <span className="rounded-full bg-agora-light/80 px-2 py-0.5 text-xs font-medium text-agora-dark">
                    Available for rent
                  </span>
                )}
                {(selectedLot.avg_utilization != null || selectedLot.estimated_capacity != null) && (
                  <span className="text-sm text-[#6b7280]">
                    {selectedLot.avg_utilization != null && `${Math.round(selectedLot.avg_utilization)}% use`}
                    {selectedLot.avg_utilization != null && selectedLot.estimated_capacity != null && " · "}
                    {selectedLot.estimated_capacity != null && `${selectedLot.estimated_capacity} spots`}
                  </span>
                )}
              </div>
              <p className="mt-2 font-medium text-[#1a1a1a]">{selectedLot.name}</p>
              <p className="text-sm text-[#6b7280] line-clamp-2">{selectedLot.address}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
