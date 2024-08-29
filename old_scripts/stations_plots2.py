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
data_hadisst_1982_2014=data_hadisst["sic"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
data_ostia_1982_2014=data_ostia["sea_ice_fraction"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
data_oisst_1982_2014=data_oisst["ice"].resample(time="MS").mean().sel(time=slice("1982", "2014"))


# Define the sub-regions with their latitude and adjusted longitude ranges
regions = {
    #'gom': {'lat': slice(39.93, 44.68), 'lon': slice(289.01, 294.25)},
    #'wss': {'lat': slice(42.14, 44.48), 'lon': slice(294.01, 296.01)},
    #'css': {'lat': slice(42.81, 44.92), 'lon': slice(296.01, 298.00)},
    #'ess': {'lat': slice(42.99, 46.38), 'lon': slice(298.00, 302.81)},
    'gsl': {'lat': slice(44.47, 51.78), 'lon': slice(292.79, 303.81)},
    'sns': {'lat': slice(42.80, 47.80), 'lon': slice(301.64, 312.28)},
    'cns': {'lat': slice(45.99, 49.25), 'lon': slice(305.51, 312.85)},
    'nns': {'lat': slice(49.24, 52.25), 'lon': slice(303.27, 309.90)},
    'sls': {'lat': slice(52.24, 57.66), 'lon': slice(298.30, 308.85)},
    'nls': {'lat': slice(57.66, 61.00), 'lon': slice(295.50, 300.50)},
    'hb': {'lat': slice(51.90, 63.96), 'lon': slice(265.31, 283.34)},
    'bb': {'lat': slice(66.64, 78.58), 'lon': slice(277.81, 309.87)},
    'bcs': {'lat': slice(47.82, 54.50), 'lon': slice(226.00, 237.49)},
    'bs': {'lat': slice(70, 75), 'lon': slice(200, 230)},
    'ao': {'lat': slice(85, 87), 'lon': slice(200, 320)},

}

#regions = {
    #'bs': {'lat': slice(70, 75), 'lon': slice(200, 230)},
    #'ao': {'lat': slice(85, 87), 'lon': slice(200, 320)},

    #'Chukchi_Sea':{'lat': slice(70, 75), 'lon': slice(180, 200)}
    #}
# Function to compute yearly mean
def compute_yearly_mean(data):
    return data.resample(time='YS').mean()

# Subset each dataset for each region and compute yearly mean
yearly_means = {}

for region, bounds in regions.items():
    yearly_means[region] = {
        'data_10_cmip6': compute_yearly_mean(data_10_ssp126_1982_2014.sel(lat=bounds['lat'], lon=bounds['lon'])),
        'data_50_cmip6': compute_yearly_mean(data_50_ssp126_1982_2014.sel(lat=bounds['lat'], lon=bounds['lon'])),
        'data_90_cmip6': compute_yearly_mean(data_90_ssp126_1982_2014.sel(lat=bounds['lat'], lon=bounds['lon'])),
        'data_hadisst': compute_yearly_mean(data_hadisst_1982_2014.sel(lat=bounds['lat'], lon=bounds['lon'])),
        'data_ostia': compute_yearly_mean(data_ostia_1982_2014.sel(lat=bounds['lat'], lon=bounds['lon'])),
        'data_oisst': compute_yearly_mean(data_oisst_1982_2014.sel(lat=bounds['lat'], lon=bounds['lon']))
    }



# Plotting for each region and dataset
for region, datasets in yearly_means.items():
    plt.figure(figsize=(12, 5))
    #datasets['data_hadisst'].mean(dim=['lat', 'lon']).plot(label='HadISST', color='red')
    #datasets['data_ostia'].mean(dim=['lat', 'lon']).plot(label='OSTIA', color='green')
    datasets['data_oisst'].mean(dim=['lat', 'lon']).fillna(0).plot(label='PIOMAS', color='blue')
    datasets['data_50_cmip6'].mean(dim=['lat', 'lon']).plot(label='CMIP6-median', color='purple')
    datasets['data_90_cmip6'].mean(dim=['lat', 'lon']).plot(label='CMIP6-90th-p', color='purple', linestyle='--')
    datasets['data_10_cmip6'].mean(dim=['lat', 'lon']).plot(label='CMIP6-10th-p', color='purple', linestyle=':')
    
    plt.title(f'{region}')
    plt.xlabel('Years')
    plt.ylabel('Sea Ice Concentration (%)')
    plt.ylim(0,100)
    plt.grid(alpha=0.3)
    plt.legend(loc= "upper right")
    
    # Save the plot
    plt.savefig(f'/home/kth097/scripts/python_script/thick/{region}_siconc.jpg', dpi=500, bbox_inches='tight')
    plt.close()
    print(f'{region} plot completed \n next')

print('====')
print('plots completed')
