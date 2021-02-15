"""
Code to help with plotting grids on cartopy maps.

"""
import cartopy.crs as ccrs
from cartopy.io import srtm
import matplotlib.pyplot as plt

from cartopy.io import PostprocessedRasterSource, LocatedImage
from cartopy.io.srtm import SRTM3Source, SRTM1Source

from functools import partial


def shade(located_elevations, azimuth, altitude):
    """
    Given an array of elevations in a LocatedImage, add a relief (shadows) to
    give a realistic 3d appearance.

    """
    new_img = srtm.add_shading(located_elevations.image,
                               azimuth=azimuth, altitude=altitude)
    return LocatedImage(new_img, located_elevations.extent)


def add_srtm_shaded(
    ax, 
    Source=SRTM1Source, 
    azimuth=135, 
    altitude=35, 
    cmap="Greys",
    **kwargs
):
    shader = partial(shade, azimuth=azimuth, altitude=altitude)
    
    shaded_srtm = PostprocessedRasterSource(Source(), shader)
    ax.add_raster(shaded_srtm, cmap=cmap, **kwargs)

    return
