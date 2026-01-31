/** Parking lot from API - matches backend ParkingLotListResponse */
export interface ParkingLot {
  id: number;
  place_id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  phone_number: string | null;
  website: string | null;
  popular_times: Record<string, number[]> | null;
  avg_utilization: number | null;
  underutilized_hours: number | null;
  rating: number | null;
  user_ratings_total: number | null;
  business_status: string | null;
  last_synced_at: string | null;
  is_available_for_rent: boolean | null;
  contact_notes: string | null;
  estimated_capacity: number | null;
  created_at: string;
  updated_at: string;
}
