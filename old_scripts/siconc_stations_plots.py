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


cmip6_path="/gpfs/fs7/eccc/cccs/kth097/SIC_data/CMIP6/percentiles/"
hadisst_path="/gpfs/fs7/eccc/cccs/kth097/SIC_data/HadISST/"
ostia_path="/gpfs/fs7/eccc/cccs/kth097/SIC_data/OSTIA_copernicus/"
oisst_path="/gpfs/fs7/eccc/cccs/kth097/SIC_data/OISST_NOAA/"
station_path="/gpfs/fs7/eccc/cccs/kth097/stations_polygon/"
#opening data


data_10_ssp126 = xr.open_dataset(cmip6_path+"siconc_hist_ssp126_10-p.nc")
data_50_ssp126 = xr.open_dataset(cmip6_path+"siconc_hist_ssp126_50-p.nc")
data_90_ssp126 = xr.open_dataset(cmip6_path+"siconc_hist_ssp126_90-p.nc")

# observed data
data_hadisst = xr.open_dataset(hadisst_path+"HadISST_siconc_interpolated.nc")*100
data_ostia = xr.open_dataset(ostia_path+"OSTIA_siconc_interpolated.nc")*100
data_oisst = xr.open_dataset(oisst_path+"OISST_siconc_interpolated.nc").isel(zlev=0)*100

# selecting var sea ice concentration for 1982 to 2014 for ssp126
data_10_ssp126_1982_2014=data_10_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_50_ssp126_1982_2014=data_50_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_90_ssp126_1982_2014=data_90_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_hadisst_1982_2014=data_hadisst["sic"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
data_ostia_1982_2014=data_ostia["sea_ice_fraction"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
data_oisst_1982_2014=data_oisst["ice"].resample(time="MS").mean().sel(time=slice("1982", "2014"))

# station
station=pd.read_csv(station_path+"polygon_nns_subarea_nns.csv", header=None, names=['lon', 'lat'])
station['lon'] = station['lon'].apply(lambda lon: lon + 360 if lon < 0 else lon)
station_polygon = Polygon(station.values)

# Create a function to check if a point is within the Hudson Bay polygon
def is_in_station(lon, lat):
    return Point(lon, lat).within(station_polygon)

# Function to compute yearly mean and mask
def compute_yearly_mean_and_mask_station(data):
    yearly_mean=data.resample(time='YS').mean()
    mask = xr.apply_ufunc(
            is_in_station,
            yearly_mean['lon'], yearly_mean['lat'],
            vectorize=True,
            dask='parallelized',
            output_dtypes=[bool])

    station_data = yearly_mean.where(mask, drop=True)
    return station_data


station_data_10_cmip6=compute_yearly_mean_and_mask_station(data_10_ssp126_1982_2014)
station_data_50_cmip6=compute_yearly_mean_and_mask_station(data_50_ssp126_1982_2014)
station_data_90_cmip6=compute_yearly_mean_and_mask_station(data_90_ssp126_1982_2014)
station_data_hadisst=compute_yearly_mean_and_mask_station(data_hadisst_1982_2014)
station_data_ostia=compute_yearly_mean_and_mask_station(data_ostia_1982_2014)
station_data_oisst=compute_yearly_mean_and_mask_station(data_oisst_1982_2014)


plt.figure(figsize=(12, 5))
station_data_hadisst.mean(dim=['lat', 'lon']).plot(label='HadISST', color='red')
station_data_ostia.mean(dim=['lat', 'lon']).plot(label='OSTIA', color='green')
station_data_oisst.mean(dim=['lat', 'lon']).fillna(0).plot(label='OISST', color='blue')
station_data_50_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-median', color='purple')
station_data_90_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-90th-p', color='purple', linestyle='--')
station_data_10_cmip6.mean(dim=['lat', 'lon']).plot(label='CMIP6-10th-p', color='purple', linestyle=':')
    
plt.title(f'North Newfoundland Shelf')
plt.xlabel('Years')
plt.ylabel('Sea Ice Concentration (%)')
plt.ylim(0,100)
plt.grid(alpha=0.3)
plt.legend(loc= "upper right")

# Save the plot
plt.savefig('nns_siconc.jpg', dpi=500, bbox_inches='tight')
plt.show()


