import os
from awx import Awx
import argparse
import matplotlib.pyplot as plt

def generate_png_for_fy2g_satellite_awx_file(raw_satellite_awx_file_path, output_png_file_path=None):
    # fpath = r'./temp/ANI_VIS_R01_20241105_1500_FY2G.AWX'  # lambert
    ds = Awx(pathfile=raw_satellite_awx_file_path)
    # print(ds)
    dar = ds.values.squeeze()
    
    plt.pcolormesh(dar.lon, dar.lat, dar, cmap='Greys_r')
    # print(f"lon:{dar.lon}, lat:{dar.lat}")
    # Remove the axis
    plt.axis('off')

    if not output_png_file_path:
        output_png_file_path = os.path.splitext(raw_satellite_awx_file_path)[0] + ".png"
    
    print(output_png_file_path)

    if(os.path.exists(output_png_file_path)):
        os.remove(output_png_file_path)

    plt.savefig(output_png_file_path, dpi=300, bbox_inches='tight', pad_inches=0, transparent=True)


def main():
    parser = argparse.ArgumentParser(description="A tool that analyse and generate 5 kinds of FY2G satellite images.")
    
    # Adding arguments
    parser.add_argument("satellite_awx_file_path", type=str, help="卫星.AWX文件路径")
    parser.add_argument("--output_png_file_path", type=str, help="输出png文件路径")
    
    # Parsing arguments
    args = parser.parse_args()

    generate_png_for_fy2g_satellite_awx_file(args.satellite_awx_file_path, args.output_png_file_path)


if __name__ == "__main__":
    main()
