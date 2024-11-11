# A simple script for generating webgis images from FY2G satellite files(.AWX) from MICAPS

## How to package
```bash
pyinstaller --onefile satellite_tool.py --console
pyinstaller --onefile awx_tool.py --console
```

## How to view on local web gis:
    ```bash
    cd temp
    python3 -m http.server 8000
    ```
    Then go to browser, and open the following url:
    http://localhost:8000/index.html

## How to extract EPSG:4326 GeoTiff from AWX
```bash
python .\test3.py .\temp\ANI_VIS_R01_20241105_1500_FY2G.AWX
```

## Coordinates of the tif
[[6.59, 77.32], [62.06, 148.7]]

## How to convert EPSG:4326 of Lambert Conformal Conic(lcc) projection to EPSG:3857 webgis tile
```bash
gdal_translate -a_srs EPSG:4326 -a_ullr 77.32 62.06 148.70 6.59 ./temp/ANI_VIS_R01_20241105_1500_FY2G_cog.tif ./temp/ANI_VIS_R01_20241105_1500_FY2G_cog_projected.tif
gdalwarp -t_srs EPSG:3857 ./temp/ANI_VIS_R01_20241105_1500_FY2G_cog_projected.tif ./temp/ANI_VIS_R01_20241105_1500_FY2G_cog_projected2.tif
```