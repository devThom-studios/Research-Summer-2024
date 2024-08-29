

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

cmip6_path = "/gpfs/fs7/eccc/cccs/kth097/SIT_data/CMIP6/sithick_can/percentiles/"
piomas_path = "/gpfs/fs7/eccc/cccs/kth097/SIT_data/PIOMAS/"
c3s_path = "/gpfs/fs7/eccc/cccs/kth097/SIT_data/copernicus_marine/"
station_path = "/gpfs/fs7/eccc/cccs/kth097/stations_polygon/"

# Load data
data_10_ssp126 = xr.open_dataset(cmip6_path + "sithick_hist_ssp126_10-p.nc")
data_50_ssp126 = xr.open_dataset(cmip6_path + "sithick_hist_ssp126_50-p.nc")
data_90_ssp126 = xr.open_dataset(cmip6_path + "sithick_hist_ssp126_90-p.nc")

data_piomas = xr.open_dataset(piomas_path + "PIOMAS_sithick_interpolated.nc")
data_c3s = xr.open_dataset(c3s_path + "c3s_sithick_interpolated.nc")

# Select time slices
data_10_ssp126_1982_2014 = data_10_ssp126["sithick"].sel(time=slice("1982", "2014"))
data_50_ssp126_1982_2014 = data_50_ssp126["sithick"].sel(time=slice("1982", "2014"))
data_90_ssp126_1982_2014 = data_90_ssp126["sithick"].sel(time=slice("1982", "2014"))

data_piomas_1982_2014 = data_piomas["sithick"].sel(time=slice("1982", "2014"))
data_c3s_2003_2014 = data_c3s["sea_ice_thickness"].sel(time=slice("2003", "2014"))

# Function to compute yearly mean and mask
def compute_yearly_mean_and_mask_station(data, station_polygon):
    yearly_mean = data.resample(time='YS').mean()
    mask = xr.apply_ufunc(
        lambda lon, lat: Point(lon, lat).within(station_polygon),
        yearly_mean['lon'], yearly_mean['lat'],
        vectorize=True,
        dask='parallelized',
        output_dtypes=[bool]
    )
    station_data = yearly_mean.where(mask, drop=True)
    return station_data

# List of station files
station_files = [
    "polygon_ao_subarea_ao.csv",
    "polygon_bs_subarea_bs.csv",
    "polygon_hb_subarea_hb.csv",
    "polygon_nns_subarea_nns.csv",
    "polygon_bb_subarea_bb.csv",
    "polygon_gsl_subarea_gsl.csv",
    "polygon_nls_subarea_nls.csv",
    "polygon_sls_subarea_sls.csv"
]

# Loop over each station
for station_file in station_files:
    station_name = station_file.split('_')[1]

    # Load station polygon
    station = pd.read_csv(station_path + station_file, header=None, names=['lon', 'lat'])
    station['lon'] = station['lon'].apply(lambda lon: lon + 360 if lon < 0 else lon)
    station_polygon = Polygon(station.values)

    # Compute station-specific data
    station_data_10_cmip6 = compute_yearly_mean_and_mask_station(data_10_ssp126_1982_2014, station_polygon)
    station_data_50_cmip6 = compute_yearly_mean_and_mask_station(data_50_ssp126_1982_2014, station_polygon)
    station_data_90_cmip6 = compute_yearly_mean_and_mask_station(data_90_ssp126_1982_2014, station_polygon)
    station_data_piomas = compute_yearly_mean_and_mask_station(data_piomas_1982_2014, station_polygon)
    station_data_c3s = compute_yearly_mean_and_mask_station(data_c3s_2003_2014, station_polygon)

    # Plotting
    plt.figure(figsize=(12, 5))
    station_data_piomas.mean(dim=['lat', 'lon']).plot(label='PIOMAS', color='red')
    if station_name=='sls':
        station_data_c3s.mean(dim=['lat', 'lon']).fillna(0).plot(label='C3S', color='green')
    else:
        station_data_c3s.mean(dim=['lat', 'lon']).plot(label='C3S', color='green')
    station_data_50_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-median', color='purple')
    station_data_90_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-90th-p', color='purple', linestyle='--')
    station_data_10_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-10th-p', color='purple', linestyle=':')

    plt.title(f'Sea Ice Thickness at {station_name}')
    plt.xlabel('Years')
    plt.ylabel('Sea Ice Thickness (m)')
    if station_name == 'gsl':
        plt.ylim(0,1.4)
    elif station_name in ['ao', 'bs']:
        plt.ylim(0,6)
    else:
        plt.ylim(0, 2.5)
    plt.grid(alpha=0.3)
    if station_name in ['ao','bb']:
        plt.legend(loc="lower left")
    else:
        plt.legend(loc="upper right")

    # Save the plot
   # plt.savefig(f'{station_name}_sithick.jpg', dpi=500, bbox_inches='tight')
    plt.savefig(f'/home/kth097/scripts/python_script/new_figures/{station_name}_sithick.jpg', dpi=500, bbox_inches='tight')

    #plt.show()

