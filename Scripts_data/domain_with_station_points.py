import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf

# Define the rotated pole projection
rotated_pole = ccrs.RotatedPole(pole_latitude=42.5, pole_longitude=83)

# Sub-regions with their latitude and longitude ranges and name offset
regions = {
    'gsl': {'lat': (44.47 + 51.78) / 2, 'lon': (-67.21 + -56.19) / 2, 'text_offset': (1.3, -1.4)},
    'nns': {'lat': (49.24 + 52.25) / 2, 'lon': (-56.73 + -50.10) / 2, 'text_offset': (1.1, -1.01)},
    'sls': {'lat': (52.24 + 57.66) / 2, 'lon': (-61.7 + -51.15) / 2, 'text_offset': (1.3, -1)},
    'nls': {'lat': (57.66 + 61.00) / 2, 'lon': (-64.50 + -59.50) / 2, 'text_offset': (1.5, -0.9)},
    'hb': {'lat': (51.90 + 63.96) / 2, 'lon': (-94.69 + -76.66) / 2, 'text_offset': (1.6, -0.6)},
    'bb': {'lat': (66.64 + 78.58) / 2, 'lon': (-82.19 + -50.13) / 2, 'text_offset': (2, -0.8)},
    'bs': {'lat': (69.09 + 76.20) / 2, 'lon': (-156.63 + -122.79) / 2,  'text_offset': (2.7, 0)},
    'ao': {'lat': (81.59 + 84.91) / 2, 'lon': (-111.95 + -79.78) / 2, 'text_offset':(5, 0.0)},
}

# Plot the data
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=rotated_pole)

# Add map features
ax.set_extent([-149, -37, 40.5, 89.97], crs=ccrs.PlateCarree())
ax.coastlines(zorder=2, linewidth=0.5)
#ax.add_feature(cf.LAND)
ax.add_feature(cf.STATES.with_scale('10m'), linewidth=0.5, zorder=2)
ax.add_feature(cf.RIVERS.with_scale('50m'), zorder=2, alpha=0.3)
ax.add_feature(cf.OCEAN.with_scale('50m'), color='white')
#ax.stock_img()



# Add the points for each station and adjust label positions
for region, coords in regions.items():
    lat = coords['lat']
    lon = coords['lon']
    text_offset = coords['text_offset']
    
    ax.plot(lon, lat, marker='o', color='red', markersize=8, transform=ccrs.PlateCarree())
    ax.text(lon + text_offset[0], lat + text_offset[1], region.upper(), transform=ccrs.PlateCarree(), fontsize=11)

#plt.title('Locations of Sea Ice Stations')
plt.savefig('domain_stations.jpg', dpi=500, bbox_inches='tight')
plt.show()

