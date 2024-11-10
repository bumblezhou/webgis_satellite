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