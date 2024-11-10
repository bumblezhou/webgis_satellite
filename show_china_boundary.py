import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load the China boundary shapefile
# Replace 'china_boundary.shp' with the path to your downloaded shapefile
china_shapefile_path = './china-shapefiles/shapefiles/china.shp'
china = gpd.read_file(china_shapefile_path)

# Set up a plot with Cartopy's projection
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([73.5, 135, 18, 53], crs=ccrs.PlateCarree())  # Set to the extent of China

# Add natural features
ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
ax.add_feature(cfeature.COASTLINE, edgecolor='black')

# Plot the China boundaries
china.plot(ax=ax, edgecolor='gray', facecolor='none', linewidth=1)

# Additional customizations
ax.set_title("China Boundaries")
# ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Show the plot
plt.show()