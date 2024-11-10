import os
from awx import Awx
from osgeo import gdal, osr
import numpy as np
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


def main():
    raw_satellite_awx_file_path = r'./temp/ANI_VIS_R01_20241105_1500_FY2G.AWX'  # lambert
    ds = Awx(pathfile=raw_satellite_awx_file_path)
    print(ds)
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

    flipped_data = np.flipud(dar.data)
    flipped_data = np.nan_to_num(flipped_data, nan=-9999)  # Replace NaNs with 0 or any preferred value

    # GeoTIFF output path
    output_tif_path = os.path.splitext(os.path.basename(raw_satellite_awx_file_path))[0] + '.tif'

    no_of_bands = 1
    # Create the GeoTIFF driver
    driver = gdal.GetDriverByName("GTiff")
    dst_ds = driver.Create(output_tif_path, width, height, no_of_bands, gdal.GDT_Byte)

    # Create a color table and define colors for various data ranges
    color_table = gdal.ColorTable()

    # # Define color entries (value, (R, G, B, A))
    # for i in range(0, 50):
    #     color_table.SetColorEntry(i, (0, 0, int(255 * (i / 50)), 255))  # Dark to light blue

    # for i in range(50, 100):
    #     color_table.SetColorEntry(i, (0, int(255 * ((i - 50) / 50)), 0, 255))  # Dark to light green

    # for i in range(100, 150):
    #     color_table.SetColorEntry(i, (int(255 * ((i - 100) / 50)), int(255 * ((i - 100) / 50)), 0, 255))  # Yellow shades

    # for i in range(150, 200):
    #     color_table.SetColorEntry(i, (int(255 * ((i - 150) / 50)), int(128 * ((i - 150) / 50)), 0, 255))  # Orange to red

    # for i in range(200, 221):  # Max value is 220
    #     color_table.SetColorEntry(i, (255, 255, 255, 255))  # White

    # Set grayscale colors for the range from 0 to 220
    # for i in range(0, 221):  # 0 (black) to 220 (light gray)
    #     gray_value = int(255 * (i / 220))  # Scale grayscale values from 0 to 220
    #     color_table.SetColorEntry(i, (gray_value, gray_value, gray_value, 255))  # Opaque gray

    # # Set grayscale colors for the range from 0 to 220
    # for i in range(0, 221):  # 0 (black) to 220 (light gray)
    #     gray_value = int(255 * (i / 220))  # Scale grayscale values from 0 to 220
    #     color_table.SetColorEntry(i, (gray_value, gray_value, gray_value))  # Grayscale RGB

    # Set the color for 255 to be fully transparent
    color_table.SetColorEntry(255, (0, 0, 0, 0))

    # Set geotransform
    dst_ds.SetGeoTransform(geotransform)

    # Write array data to band 1
    band = dst_ds.GetRasterBand(1)
    band.SetRasterColorTable(color_table)
    band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
    band.WriteArray(flipped_data)
    dst_ds.FlushCache()

    # Apply the spatial reference to the dataset
    out_srs = osr.SpatialReference()
    out_srs.ImportFromEPSG(4326) # WGS84 WGS（World Geodetic System）即世界大地测量系统，GPS 坐标系
    dst_ds.SetProjection(out_srs.ExportToWkt())
    dst_ds = None

    output_cog_file_path = os.path.splitext(os.path.basename(output_tif_path))[0] + '_cog.tif'
    convert_to_cog(output_tif_path, output_cog_file_path)

if __name__ == "__main__":
    main()
