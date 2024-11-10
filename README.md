# A simple script for generating webgis images from FY2G satellite files(.AWX) from MICAPS

## How to package
## 生成pycwr_tool可执行文件
pyinstaller --onefile satellite_tool.py --console
pyinstaller --onefile awx_tool.py --console