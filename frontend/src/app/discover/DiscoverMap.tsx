"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  GoogleMap,
  InfoWindow,
  Marker,
  useJsApiLoader,
} from "@react-google-maps/api";
import type { DiscoverSite } from "./sample-data";

const mapContainerStyle = {
  width: "100%",
  height: "100%",
};

const defaultCenter = {
  lat: 39.8283,
  lng: -98.5795,
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
  sites: DiscoverSite[];
  selectedSite: DiscoverSite | null;
  onSelectSite: (site: DiscoverSite) => void;
}

export function DiscoverMap({
  sites,
  selectedSite,
  onSelectSite,
}: DiscoverMapProps) {
  const mapRef = useRef<google.maps.Map | null>(null);
  const [infoWindowSite, setInfoWindowSite] = useState<DiscoverSite | null>(
    selectedSite
  );


  const { isLoaded, loadError } = useJsApiLoader({
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAP_API_KEY ?? "",
  });

  const onMapLoad = useCallback((map: google.maps.Map) => {
    mapRef.current = map;
  }, []);

  useEffect(() => {
    if (selectedSite && mapRef.current) {
      mapRef.current.panTo({ lat: selectedSite.lat, lng: selectedSite.lng });
      mapRef.current.setZoom(14);
      setInfoWindowSite(selectedSite);
    }
  }, [selectedSite?.id]);

  const onMarkerClick = useCallback(
    (site: DiscoverSite) => {
      onSelectSite(site);
      setInfoWindowSite(site);
      mapRef.current?.panTo({ lat: site.lat, lng: site.lng });
      mapRef.current?.setZoom(14);
    },
    [onSelectSite]
  );

  const onInfoWindowClose = useCallback(() => {
    setInfoWindowSite(null);
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
        selectedSite
          ? { lat: selectedSite.lat, lng: selectedSite.lng }
          : defaultCenter
      }
      zoom={selectedSite ? 14 : 4}
      onLoad={onMapLoad}
      options={mapOptions}
    >
      {sites.map((site) => (
        <Marker
          key={site.id}
          position={{ lat: site.lat, lng: site.lng }}
          onClick={() => onMarkerClick(site)}
          icon={{
            path: google.maps.SymbolPath.CIRCLE,
            scale: selectedSite?.id === site.id ? 14 : 10,
            fillColor: site.status === "funded" ? "#13714C" : "#3AB67D",
            fillOpacity: 1,
            strokeColor: "#fff",
            strokeWeight: 2,
          }}
        />
      ))}
      {infoWindowSite && (
        <InfoWindow
          position={{ lat: infoWindowSite.lat, lng: infoWindowSite.lng }}
          onCloseClick={onInfoWindowClose}
        >
          <div className="min-w-[200px] p-1">
            <p className="font-medium text-[#1a1a1a]">{infoWindowSite.name}</p>
            <p className="mt-1 text-sm text-[#6b7280]">
              {infoWindowSite.address}
            </p>
            <p className="mt-2 text-sm text-agora-dark">
              → {infoWindowSite.plannedUse}
            </p>
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  );
}
