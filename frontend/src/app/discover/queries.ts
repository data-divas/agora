import { useQuery } from "@tanstack/react-query";
import { fetchParkingLots } from "./api";

export const parkingLotKeys = {
  all: ["parking-lots"] as const,
  lists: () => [...parkingLotKeys.all, "list"] as const,
};

export function useParkingLotsQuery() {
  return useQuery({
    queryKey: parkingLotKeys.lists(),
    queryFn: fetchParkingLots,
  });
}
