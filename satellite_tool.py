import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import argparse
import json
from awx import Awx

def generate_satellite_image(raw_satellite_awx_file_path, output_png_file_path=None, output_json_file_path=None):
    # fpath = r'./temp/ANI_VIS_R01_20241105_1500_FY2G.AWX'  # lambert
    ds = Awx(pathfile=raw_satellite_awx_file_path)
    print(ds)
    dar = ds.values.squeeze()
    # print(dar)

    plt.figure(figsize=(8, 8))

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
    ax = plt.axes(projection=proj)
    ax.set_extent(extent, crs=proj)
    # ax.coastlines(resolution='110m')
    # ax.gridlines(draw_labels=True)
    ax.pcolormesh(dar.x, dar.y, dar, cmap='Greys_r')

    if output_png_file_path is None:
        output_png_file_path = os.path.splitext(raw_satellite_awx_file_path)[0] + ".png"
    if output_json_file_path is None:
        output_json_file_path = os.path.splitext(raw_satellite_awx_file_path)[0] + ".json"
    min_lon, max_lon = dar.ul_lon/100., dar.lr_lon/100.    # Longitude range for example
    min_lat, max_lat = dar.ul_lat/100., dar.lr_lat/100.    # Latitude range for example
    width  = dar.width                       # Width in pixels
    height = dar.height                      # Height in pixels
    data = {
        "name": "卫星图像坐标信息",
        "min_lon": min_lon,
        "min_lat": max_lat,
        "max_lon": max_lon,
        "max_lat": min_lat
    }

    if(os.path.exists(output_json_file_path)):
        os.remove(output_json_file_path)
    # Exporting the object to a JSON file
    with open(output_json_file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    # Remove the axis
    plt.axis('off')

    plt.savefig(output_png_file_path, dpi=300, bbox_inches='tight', pad_inches=0)

    # plt.show()


def main():
    parser = argparse.ArgumentParser(description="A tool that analyse and generate 5 kinds of FY2G satellite images.")
    
    # Adding arguments
    parser.add_argument("satellite_awx_file_path", type=str, help="卫星.AWX文件路径")
    parser.add_argument("--output_png_path", type=str, help="输出png文件路径")
    parser.add_argument("--output_json_path", type=str, help="输出json文件路径")
    
    # Parsing arguments
    args = parser.parse_args()

    generate_satellite_image(args.satellite_awx_file_path, args.output_png_path, args.output_json_path)

if __name__ == "__main__":
    main()