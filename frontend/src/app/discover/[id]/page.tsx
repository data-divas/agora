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
    <section className="rounded-xl bg-white/20 p-5 shadow-sm backdrop-blur-xl">
      <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-[#6b7280]">
        {title}
      </h2>
      {children}
    </section>
  );
}

function StatRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex justify-between gap-4 py-2.5 text-sm">
      <span className="text-[#6b7280]">{label}</span>
      <span className="font-medium text-[#1a1a1a] text-right">{value}</span>
    </div>
  );
}

function UtilizationBar({ value }: { value: number }) {
  const pct = Math.min(100, Math.max(0, Math.round(value)));
  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="text-[#6b7280]">Average utilization</span>
        <span className="font-semibold text-[#1a1a1a]">{pct}%</span>
      </div>
      <div className="h-2.5 w-full overflow-hidden rounded-full bg-agora-surface">
        <div
          className="h-full rounded-full bg-agora-medium transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

function RatingStars({ rating, count }: { rating: number; count: number | null }) {
  const full = Math.floor(rating);
  const half = rating - full >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return (
    <div className="flex items-center gap-2">
      <span className="flex text-agora-medium" aria-hidden>
        {"★".repeat(full)}
        {half ? "½" : ""}
        {"☆".repeat(empty)}
      </span>
      <span className="text-sm font-medium text-[#1a1a1a]">{rating.toFixed(1)}</span>
      {count != null && count > 0 && (
        <span className="text-sm text-[#6b7280]">({count} reviews)</span>
      )}
    </div>
  );
}

function RentabilityScore({ score }: { score: number }) {
  const pct = Math.min(100, Math.max(0, score));
  const color =
    pct >= 70 ? "bg-agora-medium" : pct >= 40 ? "bg-amber-500" : "bg-[#6b7280]";
  return (
    <div className="flex items-center gap-3">
      <div className="h-3 w-24 overflow-hidden rounded-full bg-agora-surface">
        <div
          className={`h-full rounded-full ${color} transition-all duration-500`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-sm font-semibold text-[#1a1a1a]">{score}/100</span>
    </div>
  );
}

function SidebarLayout() {
  return (
    <aside className="flex w-16 flex-col items-center bg-white/15 py-6 backdrop-blur-xl backdrop-saturate-150">
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
  );
}

function ErrorOrInvalid({ message, onBack }: { message: string; onBack: () => void }) {
  return (
    <div className="flex min-h-screen flex-col bg-[#FAFAFA]">
      <SidebarLayout />
      <div className="flex flex-1 items-center justify-center p-8">
        <div className="text-center">
          <p className="text-[#6b7280]">{message}</p>
          <button
            type="button"
            onClick={onBack}
            className="mt-4 text-agora-medium hover:underline font-medium"
          >
            Back to Discover
          </button>
        </div>
      </div>
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
      <ErrorOrInvalid
        message="Invalid parking lot ID."
        onBack={() => router.push("/discover")}
      />
    );
  }

  if (isLoading) return null;

  if (error || !lot) {
    return (
      <ErrorOrInvalid
        message={error instanceof Error ? error.message : "Parking lot not found."}
        onBack={() => router.push("/discover")}
      />
    );
  }

  const detail = lot as ParkingLotDetail;
  const hasOverview =
    detail.avg_utilization != null ||
    detail.underutilized_hours != null ||
    detail.estimated_capacity != null ||
    detail.rating != null ||
    detail.business_status != null;
  const googleMapsUrl = `https://www.google.com/maps?q=${encodeURIComponent(detail.latitude + "," + detail.longitude)}`;
  const googleMapsSearchUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(detail.address)}`;

  return (
    <div className="flex min-h-screen bg-[#FAFAFA]">
      <SidebarLayout />

      <div className="flex flex-1 flex-col min-w-0">
        {/* Hero */}
        <header className="bg-white/20 px-6 py-6 backdrop-blur-xl">
          <button
            type="button"
            onClick={() => router.back()}
            className="mb-4 flex items-center gap-2 text-sm text-[#6b7280] hover:text-[#1a1a1a] transition-colors"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Discover
          </button>
          <div className="flex flex-wrap items-center gap-3">
            <h1 className="text-2xl font-semibold text-[#1a1a1a] sm:text-3xl">
              {detail.name}
            </h1>
            {detail.is_available_for_rent && (
              <span className="rounded-full bg-agora-medium px-3 py-1.5 text-sm font-medium text-white">
                Available for rent
              </span>
            )}
          </div>
          <p className="mt-2 text-[#6b7280]">{detail.address}</p>
          <div className="mt-4 flex flex-wrap items-center gap-4">
            <a
              href={googleMapsSearchUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-sm font-medium text-agora-medium hover:text-agora-dark transition-colors"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              </svg>
              View on Google Maps
            </a>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-6">
          <div className="mx-auto grid max-w-5xl gap-8 lg:grid-cols-5">
            {/* Left column */}
            <div className="space-y-6 lg:col-span-3">
              <DetailSection title="Overview">
                {hasOverview ? (
                  <div className="space-y-5">
                    {detail.avg_utilization != null && (
                      <UtilizationBar value={detail.avg_utilization} />
                    )}
                    {detail.rating != null && (
                      <div>
                        <p className="mb-1.5 text-sm text-[#6b7280]">Rating</p>
                        <RatingStars
                          rating={detail.rating}
                          count={detail.user_ratings_total ?? null}
                        />
                      </div>
                    )}
                    <div className="divide-y divide-black/5">
                      {detail.underutilized_hours != null && (
                        <StatRow
                          label="Underutilized hours/week"
                          value={String(detail.underutilized_hours)}
                        />
                      )}
                      {detail.estimated_capacity != null && (
                        <StatRow
                          label="Estimated capacity"
                          value={`${detail.estimated_capacity} spots`}
                        />
                      )}
                      {detail.business_status && (
                        <StatRow label="Business status" value={detail.business_status} />
                      )}
                    </div>
                  </div>
                ) : (
                  <p className="text-sm text-[#6b7280]">No utilization or rating data yet.</p>
                )}
              </DetailSection>

              {(detail.phone_number || detail.website) && (
                <DetailSection title="Contact">
                  <div className="space-y-3 text-sm">
                    {detail.phone_number && (
                      <p>
                        <a
                          href={`tel:${detail.phone_number}`}
                          className="font-medium text-agora-medium hover:underline"
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
                          className="font-medium text-agora-medium hover:underline break-all"
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
                  <p className="text-sm text-[#6b7280] leading-relaxed">
                    {detail.contact_notes}
                  </p>
                </DetailSection>
              )}

              {detail.parcel && (
                <DetailSection title="Parcel & ownership">
                  <div className="space-y-4">
                    {detail.parcel.rentability_score != null && (
                      <div>
                        <p className="mb-2 text-sm text-[#6b7280]">Rentability score</p>
                        <RentabilityScore score={detail.parcel.rentability_score} />
                      </div>
                    )}
                    <div className="divide-y divide-black/5">
                      <StatRow label="APN" value={detail.parcel.apn} />
                      <StatRow label="County" value={detail.parcel.county} />
                      <StatRow label="State" value={detail.parcel.state} />
                      <StatRow label="Owner" value={detail.parcel.owner_name} />
                      <StatRow label="Owner type" value={detail.parcel.owner_type} />
                    </div>
                    {detail.parcel.rentability_notes &&
                      detail.parcel.rentability_notes.length > 0 && (
                        <div className="pt-2">
                          <p className="mb-2 text-sm text-[#6b7280]">Rentability notes</p>
                          <ul className="list-disc list-inside space-y-1 text-sm text-[#1a1a1a]">
                            {detail.parcel.rentability_notes.map((note, i) => (
                              <li key={i}>{note}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                  </div>
                </DetailSection>
              )}

              <DetailSection title="Next steps">
                <p className="text-sm text-[#6b7280] mb-4">
                  Interested in this lot for a community project? Use the contact info above or
                  return to discover more lots.
                </p>
                <div className="flex flex-wrap gap-3">
                  <Link
                    href="/discover"
                    className="rounded-lg bg-white/20 px-4 py-2.5 text-sm font-medium text-[#1a1a1a] hover:bg-white/40 transition-colors backdrop-blur-xl"
                  >
                    Back to Discover
                  </Link>
                </div>
              </DetailSection>
            </div>

            {/* Right column - map */}
            <div className="lg:col-span-2">
              <div className="sticky top-6 space-y-3">
                <div className="h-[380px] overflow-hidden rounded-xl bg-white/10 shadow-sm backdrop-blur-xl">
                  <DiscoverMap
                    lots={[detail]}
                    selectedLot={detail}
                    onSelectLot={() => {}}
                  />
                </div>
                <a
                  href={googleMapsUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block rounded-lg bg-white/20 px-4 py-2.5 text-center text-sm font-medium text-[#1a1a1a] hover:bg-white/40 transition-colors backdrop-blur-xl"
                >
                  Open in Google Maps
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
