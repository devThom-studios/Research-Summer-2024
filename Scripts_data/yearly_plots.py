import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as colors



cmip6_path="/gpfs/fs7/eccc/cccs/kth097/SIC_data/CMIP6/percentiles/"
hadisst_path="/gpfs/fs7/eccc/cccs/kth097/SIC_data/HadISST/"
ostia_path="/gpfs/fs7/eccc/cccs/kth097/SIC_data/OSTIA_copernicus/"
oisst_path="/gpfs/fs7/eccc/cccs/kth097/SIC_data/OISST_NOAA/"

#opening data

data_10_ssp126 = xr.open_dataset(cmip6_path+"siconc_hist_ssp126_10-p.nc")
data_50_ssp126 = xr.open_dataset(cmip6_path+"siconc_hist_ssp126_50-p.nc")
data_90_ssp126 = xr.open_dataset(cmip6_path+"siconc_hist_ssp126_90-p.nc")

# observed data
data_hadisst = xr.open_dataset(hadisst_path+"HadISST_siconc_interpolated.nc")*100
data_ostia = xr.open_dataset(ostia_path+"OSTIA_siconc_interpolated.nc")*100
data_oisst = xr.open_dataset(oisst_path+"OISST_NOAA_sea_ice_can.nc").isel(zlev=0)*100
data_oisst = xr.open_dataset(oisst_path+"OISST_siconc_interpolated.nc").isel(zlev=0)*100

# selecting var sea ice concentration for 1982 to 2014 for ssp126
data_10_ssp126_1982_2014=data_10_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_50_ssp126_1982_2014=data_50_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_90_ssp126_1982_2014=data_90_ssp126["siconc"].sel(time=slice("1982", "2014"))

# mean
yearly_data_10_ssp126_1982_2014=data_10_ssp126_1982_2014.groupby('time.year').mean('time').mean(dim=['lat','lon'])
yearly_data_50_ssp126_1982_2014=data_50_ssp126_1982_2014.groupby('time.year').mean('time').mean(dim=['lat','lon'])
yearly_data_90_ssp126_1982_2014=data_90_ssp126_1982_2014.groupby('time.year').mean('time').mean(dim=['lat','lon'])


# selecting var sea ice concentration for 1982 to 2014 for observed data/ resampling into monthly
data_hadisst_1982_2014=data_hadisst["sic"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
data_ostia_1982_2014=data_ostia["sea_ice_fraction"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
data_oisst_1982_2014=data_oisst["ice"].resample(time="MS").mean().sel(time=slice("1982", "2014"))

# mean
yearly_data_hadisst_1982_2014=data_hadisst_1982_2014.groupby('time.year').mean('time').mean(dim=['lat','lon'])
yearly_data_ostia_1982_2014=data_ostia_1982_2014.groupby('time.year').mean('time').mean(dim=['lat','lon'])
yearly_data_oisst_1982_2014=data_oisst_1982_2014.groupby('time.year').mean('time').fillna(0).mean(dim=['lat','lon'])



#plotting
# Plotting the yearly means for all datasets in a single plot
plt.figure(figsize=(12, 8))

# CMIP6 data (SSP126)
plt.plot(yearly_data_10_ssp126_1982_2014.year, yearly_data_10_ssp126_1982_2014, linestyle="-", label='CMIP6 10th-p', color='blue')
plt.plot(yearly_data_50_ssp126_1982_2014.year, yearly_data_50_ssp126_1982_2014, linestyle="--", label='CMIP6 50th-p', color='blue')
plt.plot(yearly_data_90_ssp126_1982_2014.year, yearly_data_90_ssp126_1982_2014,linestyle= 'dotted', label='CMIP6 90th-p', color='blue')

# Observed data
plt.plot(yearly_data_hadisst_1982_2014.year, yearly_data_hadisst_1982_2014, label='HadISST', color='green')
plt.plot(yearly_data_ostia_1982_2014.year, yearly_data_ostia_1982_2014, label='OSTIA', color='red')
plt.plot(yearly_data_oisst_1982_2014.year, yearly_data_oisst_1982_2014, label='OISST', color='purple')

# Adding labels, title, legend, and grid
plt.xlabel('Year', fontsize=15)
plt.ylabel('Sea Ice Concentration (%)', fontsize=15)
#plt.title('Yearly Mean Sea Ice Concentration (1982-2014)')
plt.legend(loc='lower left')
plt.ylim(0,50)
plt.grid(alpha=0.3)

# Show the plot
plt.savefig('yearly_mean_sic.jpg', dpi=500, bbox_inches='tight')
plt.show()

