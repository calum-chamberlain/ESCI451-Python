"""
Helpers for getting data programatically.

"""

import datetime
import requests
import pandas as pd


def get_geonet_quakes(
    min_latitude=-49.0, max_latitude=-40.0,
    min_longitude=164.0, max_longitude=182.0,
    min_magnitude=0.0, max_magnitude=9.0,
    min_depth=0.0, max_depth=500.0,
    start_time=datetime.datetime(1960, 1, 1),
    end_time=datetime.datetime(2020, 1, 1),
):
    """
    Get a dataframe of the eatrhquakes in the GeoNet catalogue.
    
    Parameters
    ----------
    min_latitude
        Minimum latitude in degrees for search
    max_latitude
        Maximum latitude in degrees for search
    min_longitude
        Minimum longitude in degrees for search
    max_longitude
        Maximum longitude in degrees for search
    min_depth
        Minimum depth in km for search
    max_depth
        Maximum depth in km for search
    min_magnitude
        Minimum magnitude for search
    max_magnitude
        Maximum magnitude for search
    start_time
        Start date and time for search
    end_time
        End date and time for search
        
    Returns
    -------
    pandas.DateFrame of resulting events
    """
    # Convert start_time and end_time to strings
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S")
    # Use the more efficient f-string formatting
    query_string = (
        "https://quakesearch.geonet.org.nz/csv?bbox="
        f"{min_longitude},{min_latitude},{max_longitude},"
        f"{max_latitude}&minmag={min_magnitude}"
        f"&maxmag={max_magnitude}&mindepth={min_depth}"
        f"&maxdepth={max_depth}&startdate={start_time}"
        f"&enddate={end_time}")
    print(f"Using query: {query_string}")
    response = requests.get(query_string)
    with open("data/earthquakes.csv", "wb") as f:
        f.write(response.content)
    earthquakes = pd.read_csv(
        "data/earthquakes.csv", 
        parse_dates=["origintime", "modificationtime"],
        dtype={"publicid": str})
    # Clean up header names...
    column_names = earthquakes.columns.to_list()
    mapper = {n: n.strip() for n in column_names}
    earthquakes.rename(columns=mapper, inplace=True)
    return earthquakes