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
