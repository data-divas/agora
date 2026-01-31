export type SiteStatus = "seeking" | "funded" | "in-progress";

export interface DiscoverSite {
  id: string;
  name: string;
  address: string;
  city: string;
  plannedUse: string;
  status: SiteStatus;
  lat: number;
  lng: number;
  fundingPercent: number;
  investors: number;
}

export const DISCOVER_SITES: DiscoverSite[] = [
  {
    id: "1",
    name: "Downtown Austin Lot",
    address: "201 E 2nd St, Austin, TX 78701",
    city: "Austin",
    plannedUse: "Community plaza & food hall",
    status: "seeking",
    lat: 30.2653,
    lng: -97.7403,
    fundingPercent: 45,
    investors: 128,
  },
  {
    id: "2",
    name: "Oakland Industrial Park",
    address: "1234 Broadway, Oakland, CA 94612",
    city: "Oakland",
    plannedUse: "Urban park & makerspace",
    status: "seeking",
    lat: 37.8044,
    lng: -122.2712,
    fundingPercent: 78,
    investors: 312,
  },
  {
    id: "3",
    name: "Denver RiNo Lot",
    address: "2700 Larimer St, Denver, CO 80205",
    city: "Denver",
    plannedUse: "Outdoor market & café",
    status: "funded",
    lat: 39.7589,
    lng: -104.9786,
    fundingPercent: 100,
    investors: 445,
  },
  {
    id: "4",
    name: "Portland Pearl District",
    address: "1320 NW Everett St, Portland, OR 97209",
    city: "Portland",
    plannedUse: "Public garden & event space",
    status: "in-progress",
    lat: 45.5302,
    lng: -122.6819,
    fundingPercent: 100,
    investors: 523,
  },
  {
    id: "5",
    name: "Seattle Capitol Hill",
    address: "1401 Broadway, Seattle, WA 98122",
    city: "Seattle",
    plannedUse: "Community plaza & pop-up retail",
    status: "seeking",
    lat: 47.6101,
    lng: -122.3221,
    fundingPercent: 23,
    investors: 67,
  },
];
