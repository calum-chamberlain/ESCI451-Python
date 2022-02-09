"""
Simple geodetic functions borrowed from ObsPy.

:author: Calum Chamberlain
"""

from geographiclib.geodesic import Geodesic


# WGS84 radius and flattening
WGS84_A = 6378137.0
WGS84_F = 1 / 298.257223563


def _check_latitude(latitude, variable_name='latitude'):
    """
    Check whether latitude is in the -90 to +90 range.
    """
    if latitude is None:
        return
    if latitude > 90 or latitude < -90:
        msg = '{} out of bounds! (-90 <= {} <=90)'.format(
            variable_name, variable_name)
        raise ValueError(msg)


def globe_distance(
    lat1: float, 
    lon1: float, 
    lat2: float,
    lon2: float
) -> float:
    """
    Compute the great circle distance in km between two points on Earth.
    
    """
    
    _check_latitude(lat1, 'lat1')
    _check_latitude(lat2, 'lat2')
    result = Geodesic(a=WGS84_A, f=WGS84_F).Inverse(lat1, lon1, lat2, lon2)

    return result['s12'] / 1000.
