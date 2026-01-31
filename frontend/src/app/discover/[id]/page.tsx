"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { DiscoverMap } from "../DiscoverMap";
import { useParkingLotQuery } from "../queries";
import type { ParkingLotDetail } from "../types";

function DetailSection({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-xl border border-black/5 bg-white p-4">
      <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-[#6b7280]">
        {title}
      </h3>
      {children}
    </div>
  );
}

function StatRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex justify-between gap-4 py-2 text-sm">
      <span className="text-[#6b7280]">{label}</span>
      <span className="font-medium text-[#1a1a1a]">{value}</span>
    </div>
  );
}

export default function ParkingLotDrillPage() {
  const params = useParams();
  const router = useRouter();
  const id = typeof params.id === "string" ? parseInt(params.id, 10) : null;
  const { data: lot, isLoading, error } = useParkingLotQuery(id ?? null);

  if (id == null || Number.isNaN(id)) {
    return (
      <div className="flex min-h-screen flex-col bg-[#FAFAFA]">
        <aside className="flex w-16 flex-col items-center border-r border-black/5 bg-white py-6">
          <Link href="/" className="mb-8 text-2xl font-semibold text-agora-dark" aria-label="Agora home">
            A
          </Link>
        </aside>
        <div className="flex flex-1 items-center justify-center p-8">
          <div className="text-center">
            <p className="text-[#6b7280]">Invalid parking lot ID.</p>
            <Link href="/discover" className="mt-4 inline-block text-agora-medium hover:underline">
              Back to Discover
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return null; // loading.tsx handles UI
  }

  if (error || !lot) {
    return (
      <div className="flex min-h-screen flex-col bg-[#FAFAFA]">
        <aside className="flex w-16 flex-col items-center border-r border-black/5 bg-white py-6">
          <Link href="/" className="mb-8 text-2xl font-semibold text-agora-dark" aria-label="Agora home">
            A
          </Link>
        </aside>
        <div className="flex flex-1 items-center justify-center p-8">
          <div className="text-center">
            <p className="text-red-600">
              {error instanceof Error ? error.message : "Parking lot not found."}
            </p>
            <Link href="/discover" className="mt-4 inline-block text-agora-medium hover:underline">
              Back to Discover
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const detail = lot as ParkingLotDetail;

  return (
    <div className="flex min-h-screen bg-[#FAFAFA]">
      {/* Left sidebar - same as discover */}
      <aside className="flex w-16 flex-col items-center border-r border-black/5 bg-white py-6">
        <Link href="/" className="mb-8 text-2xl font-semibold text-agora-dark" aria-label="Agora home">
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
          <Link
            href="/discover"
            className="rounded-lg bg-agora-light/40 p-2 text-agora-dark"
            aria-label="Discover"
          >
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </Link>
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex flex-1 flex-col min-w-0">
        {/* Back + title bar */}
        <div className="border-b border-black/5 bg-white px-6 py-4">
          <button
            type="button"
            onClick={() => router.back()}
            className="mb-3 flex items-center gap-2 text-sm text-[#6b7280] hover:text-[#1a1a1a] transition-colors"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Discover
          </button>
          <div className="flex flex-wrap items-center gap-3">
            <h1 className="text-2xl font-semibold text-[#1a1a1a]">{detail.name}</h1>
            {detail.is_available_for_rent && (
              <span className="rounded-full bg-agora-medium/90 px-3 py-1 text-sm font-medium text-white">
                Available for rent
              </span>
            )}
          </div>
          <p className="mt-2 text-[#6b7280]">{detail.address}</p>
        </div>

        <div className="flex-1 overflow-y-auto p-6">
          <div className="mx-auto grid max-w-4xl gap-6 lg:grid-cols-5">
            {/* Left column - details */}
            <div className="space-y-6 lg:col-span-3">
              <DetailSection title="Overview">
                <div className="divide-y divide-black/5">
                  {detail.avg_utilization != null && (
                    <StatRow label="Avg utilization" value={`${Math.round(detail.avg_utilization)}%`} />
                  )}
                  {detail.underutilized_hours != null && (
                    <StatRow label="Underutilized hours/week" value={String(detail.underutilized_hours)} />
                  )}
                  {detail.estimated_capacity != null && (
                    <StatRow label="Estimated capacity" value={`${detail.estimated_capacity} spots`} />
                  )}
                  {detail.rating != null && (
                    <StatRow
                      label="Rating"
                      value={
                        detail.user_ratings_total != null
                          ? `${detail.rating} (${detail.user_ratings_total} reviews)`
                          : String(detail.rating)
                      }
                    />
                  )}
                  {detail.business_status && (
                    <StatRow label="Business status" value={detail.business_status} />
                  )}
                </div>
              </DetailSection>

              {(detail.phone_number || detail.website) && (
                <DetailSection title="Contact">
                  <div className="space-y-2 text-sm">
                    {detail.phone_number && (
                      <p>
                        <a
                          href={`tel:${detail.phone_number}`}
                          className="text-agora-medium hover:underline"
                        >
                          {detail.phone_number}
                        </a>
                      </p>
                    )}
                    {detail.website && (
                      <p>
                        <a
                          href={detail.website}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-agora-medium hover:underline"
                        >
                          {detail.website}
                        </a>
                      </p>
                    )}
                  </div>
                </DetailSection>
              )}

              {detail.contact_notes && (
                <DetailSection title="Notes">
                  <p className="text-sm text-[#6b7280]">{detail.contact_notes}</p>
                </DetailSection>
              )}

              {detail.parcel && (
                <DetailSection title="Parcel">
                  <div className="divide-y divide-black/5">
                    <StatRow label="APN" value={detail.parcel.apn} />
                    <StatRow label="County" value={detail.parcel.county} />
                    <StatRow label="State" value={detail.parcel.state} />
                    <StatRow label="Owner" value={detail.parcel.owner_name} />
                    <StatRow label="Owner type" value={detail.parcel.owner_type} />
                    {detail.parcel.rentability_score != null && (
                      <StatRow label="Rentability score" value={`${detail.parcel.rentability_score}/100`} />
                    )}
                  </div>
                </DetailSection>
              )}
            </div>

            {/* Right column - map */}
            <div className="lg:col-span-2">
              <div className="sticky top-6 h-[320px] overflow-hidden rounded-xl border border-black/5 bg-agora-surface/30">
                <DiscoverMap
                  lots={[detail]}
                  selectedLot={detail}
                  onSelectLot={() => {}}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
