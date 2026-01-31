"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  GoogleMap,
  InfoWindow,
  Marker,
  useJsApiLoader,
} from "@react-google-maps/api";
import type { ParkingLot } from "./types";

const mapContainerStyle = {
  width: "100%",
  height: "100%",
};

const defaultCenter = {
  lat: 37.7829,
  lng: -122.4053,
};

const mapOptions = {
  disableDefaultUI: false,
  zoomControl: true,
  mapTypeControl: false,
  streetViewControl: false,
  fullscreenControl: true,
  styles: [
    {
      featureType: "poi",
      elementType: "labels",
      stylers: [{ visibility: "off" }],
    },
  ],
};

interface DiscoverMapProps {
  lots: ParkingLot[];
  selectedLot: ParkingLot | null;
  onSelectLot: (lot: ParkingLot) => void;
}

export function DiscoverMap({
  lots,
  selectedLot,
  onSelectLot,
}: DiscoverMapProps) {
  const mapRef = useRef<google.maps.Map | null>(null);
  const [infoWindowLot, setInfoWindowLot] = useState<ParkingLot | null>(
    selectedLot
  );

  const { isLoaded, loadError } = useJsApiLoader({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAP_API_KEY ?? "",
  });

  const onMapLoad = useCallback((map: google.maps.Map) => {
    mapRef.current = map;
  }, []);

  useEffect(() => {
    if (selectedLot && mapRef.current) {
      mapRef.current.panTo({
        lat: selectedLot.latitude,
        lng: selectedLot.longitude,
      });
      mapRef.current.setZoom(14);
      setInfoWindowLot(selectedLot);
    }
  }, [selectedLot?.id]);

  const onMarkerClick = useCallback(
    (lot: ParkingLot) => {
      onSelectLot(lot);
      setInfoWindowLot(lot);
      mapRef.current?.panTo({ lat: lot.latitude, lng: lot.longitude });
      mapRef.current?.setZoom(14);
    },
    [onSelectLot]
  );

  const onInfoWindowClose = useCallback(() => {
    setInfoWindowLot(null);
  }, []);

  if (loadError) {
    return (
      <div className="flex h-full items-center justify-center bg-agora-surface/30 text-[#6b7280]">
        Failed to load map. Check your API key.
      </div>
    );
  }

  if (!isLoaded) {
    return (
      <div className="flex h-full items-center justify-center bg-agora-surface/30">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-agora-medium border-t-transparent" />
      </div>
    );
  }

  return (
    <GoogleMap
      mapContainerStyle={mapContainerStyle}
      center={
        selectedLot
          ? { lat: selectedLot.latitude, lng: selectedLot.longitude }
          : lots.length > 0
            ? { lat: lots[0].latitude, lng: lots[0].longitude }
            : defaultCenter
      }
      zoom={selectedLot || lots.length > 0 ? 14 : 4}
      onLoad={onMapLoad}
      options={mapOptions}
    >
      {lots.map((lot) => (
        <Marker
          key={lot.id}
          position={{ lat: lot.latitude, lng: lot.longitude }}
          onClick={() => onMarkerClick(lot)}
          icon={{
            path: google.maps.SymbolPath.CIRCLE,
            scale: selectedLot?.id === lot.id ? 14 : 10,
            fillColor: lot.is_available_for_rent ? "#13714C" : "#3AB67D",
            fillOpacity: 1,
            strokeColor: "#fff",
            strokeWeight: 2,
          }}
        />
      ))}
      {infoWindowLot && (
        <InfoWindow
          position={{
            lat: infoWindowLot.latitude,
            lng: infoWindowLot.longitude,
          }}
          onCloseClick={onInfoWindowClose}
        >
          <div className="min-w-[200px] p-1">
            <p className="font-medium text-[#1a1a1a]">{infoWindowLot.name}</p>
            <p className="mt-1 text-sm text-[#6b7280]">{infoWindowLot.address}</p>
            {(infoWindowLot.avg_utilization != null ||
              infoWindowLot.estimated_capacity != null) && (
              <p className="mt-2 text-sm text-agora-dark">
                {infoWindowLot.avg_utilization != null &&
                  `${Math.round(infoWindowLot.avg_utilization)}% avg use`}
                {infoWindowLot.avg_utilization != null &&
                  infoWindowLot.estimated_capacity != null &&
                  " · "}
                {infoWindowLot.estimated_capacity != null &&
                  `${infoWindowLot.estimated_capacity} spots`}
              </p>
            )}
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  );
}
