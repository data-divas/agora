const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api";

export async function fetchParkingLots(): Promise<
  import("./types").ParkingLot[]
> {
  const res = await fetch(`${API_URL}/parking-lots/`);
  if (!res.ok) {
    throw new Error(`Failed to fetch parking lots: ${res.status}`);
  }
  return res.json();
}

export async function fetchParkingLot(
  id: number
): Promise<import("./types").ParkingLotDetail> {
  const res = await fetch(`${API_URL}/parking-lots/${id}`);
  if (!res.ok) {
    if (res.status === 404) throw new Error("Parking lot not found");
    throw new Error(`Failed to fetch parking lot: ${res.status}`);
  }
  return res.json();
}

/** Fetch project for a parking lot. Returns null if no project exists (404). */
export async function fetchProjectByParkingLot(
  parkingLotId: number
): Promise<import("./types").Project | null> {
  const res = await fetch(`${API_URL}/projects/by-parking-lot/${parkingLotId}`);
  if (res.status === 404) return null;
  if (!res.ok) throw new Error(`Failed to fetch project: ${res.status}`);
  return res.json();
}

/** Request a project for a parking lot (creates with status=pending). */
export async function requestProject(
  parkingLotId: number
): Promise<import("./types").Project> {
  const res = await fetch(`${API_URL}/projects/request`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ parking_lot_id: parkingLotId }),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Failed to request project: ${res.status}`);
  }
  return res.json();
}
