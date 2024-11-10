import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from awx import Awx
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import shapely.geometry as sgeom
import numpy as np
import matplotlib.transforms as mtransforms
import cartopy.crs as ccrs
from cartopy.io.shapereader import BasicReader
import cmaps
from matplotlib.path import Path
from cartopy.mpl.patch import geos_to_path
from mpl_toolkits.axes_grid1.inset_locator import TransformedBbox, BboxPatch, BboxConnector
import shapely.geometry as sgeom
from copy import copy
import concurrent.futures

fpath = './temp/ANI_IR1_R01_20241105_1500_FY2G.AWX'  # lambert

provinces = BasicReader('./china-shapefiles/shapefiles/china_country.shp')
# countries = BasicReader('./World_Countries/World_Countries.shp')

ds = Awx(pathfile=fpath)
print(ds)
dar = ds.values.squeeze()

if dar.projection == 1:
    proj = ccrs.LambertConformal(central_longitude=dar.clon / 100,
                                 central_latitude=dar.clat / 100,
                                 standard_parallels=(dar.std_lat1_or_lon / 100.,
                                                     dar.std_lat2 / 100.))
    extent = [dar.x.min(), dar.x.max(), dar.y.min(), dar.y.max()]
elif dar.projection == 2:
    proj = ccrs.Mercator(central_longitude=dar.clon / 100,
                         latitude_true_scale=dar.std_lat1_or_lon / 100.)
    extent = [dar.x.min(), dar.x.max(), dar.y.min(), dar.y.max()]
elif dar.projection == 4:
    proj = ccrs.PlateCarree(central_longitude=dar.clon / 100.)
    extent = [dar.lon.min(), dar.lon.max(), dar.lat.min(), dar.lat.max()]
else:
    raise NotImplementedError()
fig = plt.figure(figsize=(10, 8),dpi=100)    
ax = plt.axes(projection=proj)
ax.set_extent(extent, crs=proj)
print(proj)
ax.pcolormesh(dar.x, dar.y, dar, cmap='Greys_r')
ax.gridlines(draw_labels=True)

ax.add_geometries(provinces.geometries(), linewidth=.5, edgecolor='white', crs=ccrs.PlateCarree(),
                  facecolor='none') 
# ax.add_geometries(countries.geometries(), linewidth=.5, edgecolor='black', crs=ccrs.PlateCarree(),
# facecolor='none')
plt.savefig(os.path.splitext(os.path.basename(fpath))[0] + '.png', dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()