import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pandas as pd
import cartopy.feature as cf
inputdir1='/gpfs/fs7/eccc/cccs/kth097/stations_polygon/'
output='/home/kth097/scripts/python_script/new_figures/'

# Define the file paths for your lat/lon files
name=['ao','bs','hb','nns','bb', 'gsl', 'nls','sls']

regions = {
    'gsl': {'lat': (44.47 + 51.78) / 2, 'lon': (-67.21 + -56.19) / 2, 'text_offset': (-2, 0.0)},
    'nns': {'lat': (49.24 + 52.25) / 2, 'lon': (-56.73 + -50.10) / 2, 'text_offset': (2.8, -0.9)},
    'sls': {'lat': (52.24 + 57.66) / 2, 'lon': (-61.7 + -51.15) / 2, 'text_offset': (3, -0.8)},
    'nls': {'lat': (57.66 + 61.00) / 2, 'lon': (-64.50 + -59.50) / 2, 'text_offset': (1.9, -0.7)},
    'hb': {'lat': (51.90 + 63.96) / 2, 'lon': (-94.69 + -76.66) / 2, 'text_offset': (1.4, -0.3)},
    'bb': {'lat': (66.64 + 78.58) / 2, 'lon': (-82.19 + -50.13) / 2, 'text_offset': (2, -0.8)},
    'bs': {'lat': (69.09 + 76.20) / 2, 'lon': (-156.63 + -122.79) / 2,  'text_offset': (2.7, -0.1)},
    'ao': {'lat': (81.59 + 84.91) / 2, 'lon': (-111.95 + -79.78) / 2, 'text_offset':(-5, -0.25)},
}


csv_files = [
    "polygon_gsl_subarea_gsl.csv",
    "polygon_nns_subarea_nns.csv",
    "polygon_sls_subarea_sls.csv",
    "polygon_nls_subarea_nls.csv",
    "polygon_hb_subarea_hb.csv",
    "polygon_bb_subarea_bb.csv",
    "polygon_bs_subarea_bs.csv",
    "polygon_ao_subarea_ao.csv"
]

# Read the latitude and longitude data for each subregion
subregions = [pd.read_csv(inputdir1+file,  header=None, names=['lon', 'lat']) for file in csv_files]

# Initialize the plot
fig1 = plt.figure(figsize=(12,8))
ax=fig1.add_subplot(1,1,1, projection=ccrs.RotatedPole(pole_latitude=42.5,pole_longitude=83))

# Add map features
ax.set_extent([-149, -37, 40.5, 89.97], crs=ccrs.PlateCarree())
ax.coastlines(zorder=2, linewidth=0.5)
ax.add_feature(cf.STATES.with_scale('10m'), linewidth=0.5, zorder=2)
ax.add_feature(cf.RIVERS.with_scale('50m'), zorder=2, alpha=0.3)
ax.add_feature(cf.OCEAN.with_scale('50m'), color='white')

colors = [
    'brown', 'purple', 'magenta', 'black',
    'red', 'blue', 'green',  'orange',

]

# Plot each subregion with a different color
for subregion, color in zip(subregions, colors):
    ax.plot(subregion['lon'], subregion['lat'], marker='.', linestyle='-', markersize=0.01,
            linewidth=1.5, color=color, transform=ccrs.PlateCarree())

for region, coords in  regions.items():
    lat = coords['lat']
    lon = coords['lon']
    text_offset = coords['text_offset']
    ax.text(lon + text_offset[0], lat + text_offset[1], region,  transform=ccrs.PlateCarree(), fontsize=11)



# Add a title
#ax.set_title('8 Subregions in Ocean around Canada', fontsize=12)

plt.savefig(f'/home/kth097/scripts/python_script/new_figures/domain_stations.jpg', dpi=500, bbox_inches='tight')

# Show the plot
plt.show()
