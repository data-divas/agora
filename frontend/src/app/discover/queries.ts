import { useQuery } from "@tanstack/react-query";
import { fetchParkingLot, fetchParkingLots } from "./api";

export const parkingLotKeys = {
  all: ["parking-lots"] as const,
  lists: () => [...parkingLotKeys.all, "list"] as const,
  detail: (id: number) => [...parkingLotKeys.all, "detail", id] as const,
};

export function useParkingLotsQuery() {
  return useQuery({
    queryKey: parkingLotKeys.lists(),
    queryFn: fetchParkingLots,
  });
}

export function useParkingLotQuery(id: number | null) {
  return useQuery({
    queryKey: parkingLotKeys.detail(id ?? 0),
    queryFn: () => fetchParkingLot(id!),
    enabled: id != null && id > 0,
  });
}
