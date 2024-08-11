from shapely import Polygon
import numpy as np

def shapely_polygon_to_points_list(polygon:Polygon):
    xx,yy = polygon.exterior.coords.xy
    out = list(zip(xx,yy)) + [(xx[-1], yy[-1])]
    return np.array(out)