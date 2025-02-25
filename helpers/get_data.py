"""
Helpers for getting data programatically.

"""

import datetime
import requests
import pandas as pd
import os
import warnings
import zipfile


def download_and_extract(url, outdir=None):
    """
    Download a zipfile from the web and extract it to a directory.
    
    Parameters
    ----------
    url
        URL to remote zipfile
    outfir
        Directory to write contents to - does not have to exist
    """
    # Check that file is zip
    ext = os.path.splitext(url)[-1]
    assert ext == ".zip", f"Zip file required, extension {ext}"
    
    if outdir is None:
        outdir = os.path.splitext(url.split('/')[-1])[0]
        
    # Make it a full path
    outdir = os.path.realpath(outdir)
    archive_file = f"{outdir}.zip"
    
    response = requests.get(url)
    with open(archive_file, "wb") as f:
        f.write(response.content)

    # Make the location to put the data
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    # Extract all can be unsafe - check each path doesn't have path-traversal parts...
    with zipfile.ZipFile(archive_file, 'r') as zf:
        for member in zf.infolist():
            outfile = os.path.join(outdir, member.filename)
            # check that the file lands in the directory
            if outfile.startswith(outdir):
                zf.extract(member, outdir)
            else:
                warnings.warn(f"{member.filename} has unsafe path, skipping")
    
    
    # Cleanup
    os.remove(archive_file)
    return


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
    try:
        earthquakes = pd.read_csv(
            "data/earthquakes.csv", 
            parse_dates=["origintime", "modificationtime"],
            dtype={"publicid": str})
    except ValueError as e:
        # Missing column - usually related to issue #27 - data request too large - read contents raw
        with open("data/earthquakes.csv", "r") as f:
            contents = f.read()
            raise IOError(contents)
    # Clean up header names...
    column_names = earthquakes.columns.to_list()
    mapper = {n: n.strip() for n in column_names}
    earthquakes.rename(columns=mapper, inplace=True)
    return earthquakes


def get_gnss_for_station(
    station: str, 
    fits_url: str = "http://fits.geonet.org.nz/observation",
    starttime: datetime.datetime = None,
    endtime: datetime.datetime = None,
) -> dict:
    """
    Get GNSS data from GeoNet for the station
    
    Parameters
    ----------
    station
        The name of the station you want to get data for
    fits_url
        URL of the FITS data service you want to query.
    starttime
        Earliest timestamp to return
    endtime
        Latest timestamp to return
        
    Returns
    -------
    Dictionary with keys:
        time 
            list of timestamps of observations
        north
            list of offsets in mm in the north direction
        east
            list of offsets in mm in the east direction
        up          
            list of vertical offsets in mm
        north_error
            list of errors in mm for north
        east_error
            list of errors in mm for east
        up_error
            list of erros in mm for up
    
    """
    # Initialise an empty dictionary that we will append to
    out = dict(time=[],
               north=[],
               east=[],
               up=[],
               north_error=[],
               east_error=[],
               up_error=[])
    for channel in {"north", "east", "up"}:
        parameters = {"typeID": channel[0], "siteID": station}
        response = requests.get(fits_url, params=parameters)
        assert response.status_code == 200, "Bad request"
        payload = response.content.decode("utf-8").split("\n")
        # payload is a csv with header
        # This is a list-comprehension, a type of fast, one-line for loop
        payload = [p.split(',') for p in payload]
        # Check that this is what we expect
        assert payload[0][0] == 'date-time', "Unkown format"
        assert len(payload[0]) == 3, "Unknown format"
        times, displacements, errors = zip(*[
            (datetime.datetime.strptime(p[0], '%Y-%m-%dT%H:%M:%S.%fZ'),
             float(p[1]), float(p[2])) for p in payload[1:-1]])
        if len(out["time"]) == 0:
            out.update({"time": times})
        else:
            assert out["time"] == times, "Different time sampling for different components."
        out.update({channel: displacements, f"{channel}_error": errors})
    starttime = starttime or min(out["time"])
    endtime = endtime or max(out["time"])
    mask = [starttime <= t <=endtime for t in out["time"]]
    for key, value in out.items():
        out.update({key: [v for v, m in zip(value, mask) if m]})
    return out
