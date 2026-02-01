import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchParkingLot, fetchParkingLots, fetchProjectByParkingLot, requestProject } from "./api";

export const parkingLotKeys = {
  all: ["parking-lots"] as const,
  lists: () => [...parkingLotKeys.all, "list"] as const,
  detail: (id: number) => [...parkingLotKeys.all, "detail", id] as const,
};

export const projectKeys = {
  all: ["projects"] as const,
  byParkingLot: (parkingLotId: number) => [...projectKeys.all, "by-parking-lot", parkingLotId] as const,
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

export function useProjectByParkingLotQuery(parkingLotId: number | null) {
  return useQuery({
    queryKey: projectKeys.byParkingLot(parkingLotId ?? 0),
    queryFn: () => fetchProjectByParkingLot(parkingLotId!),
    enabled: parkingLotId != null && parkingLotId > 0,
  });
}

export function useRequestProjectMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (parkingLotId: number) => requestProject(parkingLotId),
    onSuccess: (_, parkingLotId) => {
      queryClient.invalidateQueries({ queryKey: projectKeys.byParkingLot(parkingLotId) });
    },
  });
}
