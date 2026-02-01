"""Google Maps API and popular times integration service."""

from typing import List, Optional
import logging

from fastapi import HTTPException
import requests
import populartimes

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


def fetch_places_nearby(lat: float, lng: float, radius: int) -> List[dict]:
    """
    Fetch parking lots from Google Places API using Nearby Search.

    Args:
        lat: Latitude coordinate
        lng: Longitude coordinate
        radius: Search radius in meters

    Returns:
        List of parking lot place results

    Raises:
        HTTPException: If the API request fails
    """
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "parking",
        "key": settings.google_maps_api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "OK":
            return data.get("results", [])
        elif data.get("status") == "ZERO_RESULTS":
            return []
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Google Places API error: {data.get('status')} - {data.get('error_message', 'Unknown error')}",
            )
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch parking lots: {str(e)}")


def fetch_popular_times(place_id: str) -> tuple[Optional[dict], Optional[float]]:
    """
    Fetch popular times data using the populartimes library.

    This function scrapes Google Maps to get hourly utilization data across the week.
    The data represents how busy a place is during different times.

    Args:
        place_id: Google Places place ID

    Returns:
        Tuple of (popular_times_dict, avg_utilization)
        popular_times_dict format: {"Monday": [0-100 for 24 hours], "Tuesday": [...], ...}
        avg_utilization: Average utilization percentage across all hours

    Note:
        Returns (None, None) if no data is available or if the request fails.
    """
    try:
        result = populartimes.get_id(settings.google_maps_api_key, place_id)
        popular_times_raw = result.get("populartimes", [])

        if not popular_times_raw:
            logger.info(f"No popular times data for place_id: {place_id}")
            return None, None

        # Convert to day-name based format for better readability
        day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        popular_times_dict = {}
        total_popularity = 0
        data_point_count = 0

        for day_data in popular_times_raw:
            day_index = day_data.get("day", 0)
            day_name = day_names[day_index]
            hourly_data = day_data.get("data", [])

            popular_times_dict[day_name] = hourly_data

            # Calculate running totals
            total_popularity += sum(hourly_data)
            data_point_count += len(hourly_data)

        # Calculate average utilization across all hours of the week
        avg_utilization = total_popularity / data_point_count if data_point_count > 0 else None

        if avg_utilization:
            logger.info(f"Place {place_id}: avg utilization = {avg_utilization:.1f}%")

        return popular_times_dict, avg_utilization

    except Exception as e:
        logger.warning(f"Failed to fetch popular times for {place_id}: {str(e)}")
        return None, None


def calculate_metrics(popular_times: Optional[dict]) -> tuple[Optional[float], Optional[int]]:
    """
    Calculate average utilization and underutilized hours from popular times data.

    Args:
        popular_times: Dictionary with day names as keys and hourly data (0-100) as values
                      Format: {"Monday": [10, 15, 20, ...], "Tuesday": [...], ...}

    Returns:
        Tuple of (avg_utilization, underutilized_hours)
        - avg_utilization: Average utilization percentage across all hours (0-100)
        - underutilized_hours: Number of hours per week with < 30% utilization
    """
    if not popular_times:
        return None, None

    total_popularity = 0
    data_point_count = 0
    underutilized_hours = 0

    for day_name, hourly_data in popular_times.items():
        if isinstance(hourly_data, list):
            for hour_value in hourly_data:
                total_popularity += hour_value
                data_point_count += 1
                if hour_value < 30:  # Consider < 30% as underutilized
                    underutilized_hours += 1

    avg_utilization = total_popularity / data_point_count if data_point_count > 0 else None

    return avg_utilization, underutilized_hours


def count_underutilized_hours(popular_times: Optional[dict]) -> Optional[int]:
    """
    Count the number of hours per week with utilization < 30%.

    Args:
        popular_times: Dictionary with day names as keys and hourly data as values

    Returns:
        Number of underutilized hours (< 30% utilization), or None if no data
    """
    if not popular_times:
        return None

    underutilized_hours = 0

    for day_name, hourly_data in popular_times.items():
        if isinstance(hourly_data, list):
            for hour_value in hourly_data:
                if hour_value < 30:
                    underutilized_hours += 1

    return underutilized_hours
