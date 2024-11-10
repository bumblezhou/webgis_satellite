import os
from awx import Awx
from osgeo import gdal, osr
import numpy as np
import argparse
# import pandas as pd
import json
gdal.UseExceptions()


def convert_to_cog(input_file, output_file):
    # Open the source GeoTIFF file
    src_ds = gdal.Open(input_file, gdal.GA_ReadOnly)
    if src_ds is None:
        raise FileNotFoundError(f"Cannot open input file {input_file}")

    # Define the creation options for COG
    creation_options = [
        "COMPRESS=DEFLATE",     # Or use DEFLATE for compression
        "BIGTIFF=YES",          # Optional: Ensures file compatibility if it's large
        "BLOCKSIZE=1024"        # Block size for tiling
    ]

    # Convert to COG format
    gdal.Translate(
        output_file,
        src_ds,
        format="COG",
        creationOptions=creation_options
    )

    print(f"Conversion complete: {output_file}")


def generate_json_data_for_fy2g_satellite_awx_file(raw_satellite_awx_file_path, output_json_file_path=None):
    # fpath = r'./temp/ANI_VIS_R01_20241105_1500_FY2G.AWX'  # lambert
    ds = Awx(pathfile=raw_satellite_awx_file_path)
    # print(ds)
    dar = ds.values.squeeze()
    
    # Define your latitude and longitude bounds and pixel size
    min_lon, max_lon = dar.ul_lon/100., dar.lr_lon/100.    # Longitude range for example
    min_lat, max_lat = dar.ul_lat/100., dar.lr_lat/100.    # Latitude range for example
    width  = dar.width                       # Width in pixels
    height = dar.height                      # Height in pixels

    # Calculate pixel size
    pixel_size_x = (max_lon - min_lon) / width
    pixel_size_y = (max_lat - min_lat) / height

    # Set the geotransform
    geotransform = (
        min_lon,        # top left x (longitude of the upper-left corner)
        pixel_size_x,   # pixel width (longitude)
        0,              # rotation (0 if north up)
        max_lat,        # top left y (latitude of the upper-left corner)
        0,              # rotation (0 if north up)
        -pixel_size_y   # pixel height (negative because y decreases as you go down)
    )

    # rotated_array = np.rot90(dar.data, k=1)  # k=-1 for clockwise, k=1 for counterclockwise
    # rotated_array = np.rot90(rotated_array, k=1)

    flipped_data = dar.data

    # flipped_data = np.flipud(dar.data)
    # flipped_data = np.nan_to_num(flipped_data, nan=255)  # Replace NaNs with 0 or any preferred value

    # data = {
    #     "name": "卫星图像",
    #     "width": width,
    #     "height": height,
    #     "min_lon": min_lon,
    #     "max_lon": max_lon,
    #     "min_lat": min_lat,
    #     "max_lat": max_lat,
    #     "pixel_size_x": pixel_size_x,
    #     "pixel_size_y": pixel_size_y,
    #     "data": flipped_data.tolist(),
    # }

    # if not output_json_file_path:
    #     output_json_file_path = os.path.splitext(raw_satellite_awx_file_path)[0] + ".json"
    
    # print(output_json_file_path)

    # if(os.path.exists(output_json_file_path)):
    #     os.remove(output_json_file_path)
    # # Exporting the object to a JSON file
    # with open(output_json_file_path, "w") as json_file:
    #     json.dump(data, json_file, indent=4)

    # GeoTIFF output path
    output_tif_path = os.path.splitext(os.path.basename(raw_satellite_awx_file_path))[0] + '.tif'

    no_of_bands = 1
    # Create the GeoTIFF driver
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(output_tif_path, width, height, no_of_bands, gdal.GDT_Byte)

    # Set geotransform
    dst_ds.SetGeoTransform(geotransform)

    # Write array data to band 1
    dst_ds.GetRasterBand(1).WriteArray(flipped_data)
    dst_ds.GetRasterBand(1).SetNoDataValue(255)
    dst_ds.FlushCache()

    # Apply the spatial reference to the dataset
    out_srs = osr.SpatialReference()
    out_srs.ImportFromEPSG(4326) # WGS84 WGS（World Geodetic System）即世界大地测量系统，GPS 坐标系
    # out_srs.ImportFromEPSG(3857) # WGS 84 / Pseudo-Mercator
    dst_ds.SetProjection(out_srs.ExportToWkt())
    dst_ds = None

    output_cog_file_path = os.path.splitext(raw_satellite_awx_file_path)[0] + "_cog.tif"
    convert_to_cog(output_tif_path, output_cog_file_path)


def main():
    parser = argparse.ArgumentParser(description="A tool that analyse and generate 5 kinds of FY2G satellite images.")
    
    # Adding arguments
    parser.add_argument("satellite_awx_file_path", type=str, help="卫星.AWX文件路径")
    parser.add_argument("--output_json_path", type=str, help="输出JSON文件路径")
    
    # Parsing arguments
    args = parser.parse_args()

    generate_json_data_for_fy2g_satellite_awx_file(args.satellite_awx_file_path, args.output_json_path)


if __name__ == "__main__":
    main()
