

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as colors
from shapely.geometry import Point, Polygon
import warnings
warnings.simplefilter('ignore')
import time

# Paths
cmip6_path = "/gpfs/fs7/eccc/cccs/kth097/SIC_data/CMIP6/percentiles/"
hadisst_path = "/gpfs/fs7/eccc/cccs/kth097/SIC_data/HadISST/"
ostia_path = "/gpfs/fs7/eccc/cccs/kth097/SIC_data/OSTIA_copernicus/"
station_path = "/gpfs/fs7/eccc/cccs/kth097/stations_polygon/"

# Station filenames
station_files = [
    "polygon_nns_subarea_nns.csv",
    "polygon_ao_subarea_ao.csv",
    "polygon_bs_subarea_bs.csv",
    "polygon_hb_subarea_hb.csv",
    "polygon_bb_subarea_bb.csv",
    "polygon_gsl_subarea_gsl.csv",
    "polygon_nls_subarea_nls.csv",
    "polygon_sls_subarea_sls.csv"
]

# Opening data
data_10_ssp126 = xr.open_dataset(cmip6_path + "siconc_hist_ssp126_10-p.nc")
data_50_ssp126 = xr.open_dataset(cmip6_path + "siconc_hist_ssp126_50-p.nc")
data_90_ssp126 = xr.open_dataset(cmip6_path + "siconc_hist_ssp126_90-p.nc")

# Observed data
data_hadisst = xr.open_dataset(hadisst_path + "HadISST_siconc_interpolated.nc") * 100
data_ostia = xr.open_dataset(ostia_path + "OSTIA_siconc_interpolated.nc") * 100

# Selecting var sea ice concentration for 1982 to 2014 for ssp126
data_10_ssp126_1982_2014 = data_10_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_50_ssp126_1982_2014 = data_50_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_90_ssp126_1982_2014 = data_90_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_hadisst_1982_2014 = data_hadisst["sic"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
data_ostia_1982_2014 = data_ostia["sea_ice_fraction"].resample(time="MS").mean().sel(time=slice("1982", "2014"))

# Create a function to check if a point is within a station polygon
def is_in_station(lon, lat, polygon):
    return Point(lon, lat).within(polygon)

# Function to compute yearly mean and mask station
def compute_yearly_mean_and_mask_station(data, polygon):
    yearly_mean = data.resample(time='YS').mean()
    mask = xr.apply_ufunc(
        is_in_station,
        yearly_mean['lon'], yearly_mean['lat'],
        input_core_dims=[[], []],
        kwargs={'polygon': polygon},
        vectorize=True,
        dask='parallelized',
        output_dtypes=[bool]
    )
    station_data = yearly_mean.where(mask, drop=True)
    return station_data

# Function to process and plot data for each station
def process_and_plot_station(station_file):
    station_name = station_file.split('_')[1]

    # Read station polygon
    station = pd.read_csv(station_path + station_file, header=None, names=['lon', 'lat'])
    station['lon'] = station['lon'].apply(lambda lon: lon + 360 if lon < 0 else lon)
    station_polygon = Polygon(station.values)

    # Compute masked data for the station
    station_data_10_cmip6 = compute_yearly_mean_and_mask_station(data_10_ssp126_1982_2014, station_polygon)
    station_data_50_cmip6 = compute_yearly_mean_and_mask_station(data_50_ssp126_1982_2014, station_polygon)
    station_data_90_cmip6 = compute_yearly_mean_and_mask_station(data_90_ssp126_1982_2014, station_polygon)
    station_data_hadisst = compute_yearly_mean_and_mask_station(data_hadisst_1982_2014, station_polygon)
    station_data_ostia = compute_yearly_mean_and_mask_station(data_ostia_1982_2014, station_polygon)

    # Plot
    plt.figure(figsize=(12, 5))
    station_data_hadisst.mean(dim=['lat', 'lon']).plot(label='HadISST', color='red')
    station_data_ostia.mean(dim=['lat', 'lon']).plot(label='OSTIA', color='green')
    station_data_50_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-median', color='purple')
    station_data_90_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-90th-p', color='purple', linestyle='--')
    station_data_10_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-10th-p', color='purple', linestyle=':')

    plt.title(f'Sea Ice Concentration in {station_name}')
    plt.xlabel('Years')
    plt.ylabel('Sea Ice Concentration (%)')
    if station_name=='ao':
        plt.ylim(75,105)
    else:
        plt.ylim(0, 100)
    plt.grid(alpha=0.3)
    if station_name in ['ao', 'bs', 'bb']:
        plt.legend(loc="lower left")
    else:
        plt.legend(loc="upper right")

    # Save the plot
    plt.savefig(f'/home/kth097/scripts/python_script/new_figures/{station_name}_siconc.jpg', dpi=500, bbox_inches='tight')
    plt.show()
    time.sleep(3)
# Loop through each station and generate plots
for station_file in station_files:
    process_and_plot_station(station_file)

