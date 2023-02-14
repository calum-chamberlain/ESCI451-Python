# Adapted from https://gist.github.com/joshhartmann11

import numpy as np
import pandas as pd

# Using the definition found on https://en.wikipedia.org/wiki/Esri_grid
def transform_asc_to_df(ascfile):
    N_ROWS_HEADER = 6

    # Split into header and body
    with open(ascfile, "r") as f:
        contents = f.read().splitlines()
        header, body_raw = contents[0:N_ROWS_HEADER], contents[N_ROWS_HEADER:]

    # Read the configuration from the header
    config = {}
    for i, line in enumerate(header):
        variable = header[i].strip().split(" ")[0]
        value = float(header[i].strip().split(" ")[-1])
        config[variable.lower()] = value
        
    # Hack to cope (slowly) with somewhat irregular grid
    body = np.zeros([int(config["nrows"]), int(config["ncols"])])
    
    row, col = 0, 0
    for line in body_raw:
        if line == '':
            row += 1
            col = 0
        elems = line.split()
        for elem in elems:
            body[row][col] = float(elem)
            col += 1

    # Put NAN where applicable
    body[body == config["nodata_value"]] = float('nan')

    # Generate lat lon columns
    start = config["cellsize"] / 2
    step = config["cellsize"]

    latstart = config["yllcorner"] + step / 2
    latstop = latstart + step * (config["nrows"] - 1)
    latitude = np.linspace(latstart, latstop, int(config["nrows"]))
    latitude = np.repeat(latitude, int(config["ncols"]))[::-1]

    lonstart = config["xllcorner"] + step / 2
    lonstop = lonstart + step * (config["ncols"] - 1)
    longitude = np.linspace(lonstart, lonstop, int(config["ncols"]))
    longitude = np.tile(longitude, int(config["nrows"]))

    # Generate grid points
    grid_y = np.linspace(0, config["nrows"] - 1, int(config["nrows"]))
    grid_y = np.repeat(grid_y, int(config["ncols"]))[::-1]

    grid_x = np.linspace(0, config["ncols"]-1, int(config["ncols"]))
    grid_x = np.tile(grid_x, int(config["nrows"]))

    # Flatten the body matrix
    body = body.flatten()

    # Roll into pandas dataframe
    df = pd.DataFrame({
        "longitude": longitude,
        "latitude": latitude,
        "grid_x": grid_x,
        "grid_y": grid_y,
        "variable": body})

    return df