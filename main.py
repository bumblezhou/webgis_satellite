import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from awx import Awx
from osgeo import gdal, osr
import geopandas as gpd
import cartopy.feature as cfeature
from cartopy.io.shapereader import BasicReader
gdal.UseExceptions()


def main():
    fpath = r'./temp/ANI_IR1_R01_20241105_1500_FY2G.AWX'
    ds = Awx(pathfile=fpath)
    # print(ds)
    dar = ds.values.squeeze()

    plt.pcolormesh(dar.lon, dar.lat, dar, cmap='Greys_r')
    # print(f"lon:{dar.lon}, lat:{dar.lat}")
    # Remove the axis
    plt.axis('off')
    plt.savefig(os.path.splitext(fpath)[0] + '.png', dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)
    # plt.show()

    # # draw data in projection coordination
    # fpath = r'./temp/ANI_VIS_R01_20241105_1500_FY2G.AWX'  # lambert
    # ds = Awx(pathfile=fpath)
    # print(ds)
    # dar = ds.values.squeeze()
    # # print(dar)

    # plt.figure(figsize=(8, 8))

    # if dar.projection == 1:
    #     proj = ccrs.LambertConformal(central_longitude=dar.clon / 100,
    #                                 central_latitude=dar.clat / 100,
    #                                 standard_parallels=(dar.std_lat1_or_lon / 100.,
    #                                                     dar.std_lat2 / 100.))
    #     extent = [dar.x.min(), dar.x.max(), dar.y.min(), dar.y.max()]
    # elif dar.projection == 2:
    #     proj = ccrs.Mercator(central_longitude=dar.clon / 100,
    #                         latitude_true_scale=dar.std_lat1_or_lon / 100.)
    #     extent = [dar.x.min(), dar.x.max(), dar.y.min(), dar.y.max()]
    # elif dar.projection == 4:
    #     proj = ccrs.PlateCarree(central_longitude=dar.clon / 100.)
    #     extent = [dar.lon.min(), dar.lon.max(), dar.lat.min(), dar.lat.max()]
    # else:
    #     raise NotImplementedError()
    # ax = plt.axes(projection=proj)
    # ax.set_extent(extent, crs=proj)
    # print(proj)
    # # ax.coastlines(resolution='110m')
    # ax.gridlines(draw_labels=True)
    # ax.pcolormesh(dar.x, dar.y, dar, cmap='Greys_r')
    # # Remove the axis
    # plt.axis('off')
    # plt.savefig(os.path.splitext(fpath)[0] + '.png', dpi=300, bbox_inches='tight', pad_inches=0)
    # # plt.show()


if __name__ == "__main__":
    main()