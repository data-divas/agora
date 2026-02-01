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

/** Parcel from API - matches backend ParcelResponse (optional on detail) */
export interface Parcel {
  id: number;
  apn: string;
  address: string;
  county: string;
  state: string;
  parking_lot_id: number | null;
  owner_name: string;
  owner_mailing_address: string | null;
  owner_type: string;
  is_likely_commercial: boolean;
  zoning: string | null;
  land_use: string | null;
  lot_size_sqft: number | null;
  assessed_value: number | null;
  year_built: number | null;
  geometry: Record<string, unknown> | null;
  rentability_score: number | null;
  rentability_notes: string[] | null;
}

/** Single parking lot detail - matches backend ParkingLotResponse (includes optional parcel) */
export interface ParkingLotDetail extends ParkingLot {
  parcel: Parcel | null;
}

/** Project from API - matches backend Project (e.g. for parking lot) */
export interface Project {
  id: number;
  name: string;
  required_fund: number | null;
  project_type: string | null;
  project_description: string | null;
  status: string | null;
  investment_goal: number | null;
  solana_pda_wallet: string | null;
  parking_lot_id: number | null;
  created_at: string;
  updated_at: string;
}
