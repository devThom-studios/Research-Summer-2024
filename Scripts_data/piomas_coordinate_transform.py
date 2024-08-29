import xarray as xr
import pandas as pd
import numpy as np
import time
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import time

start_time=time.time()

path='/gpfs/fs7/eccc/cccs/kth097/SIT_data/PIOMAS/'

#open data
ds=xr.open_dataset(path+'all_heff.nc')

#setting the time dimension
time_new = pd.date_range(start='1979-01-01', end='2023-12-31', freq='MS')

#Replace the existing time dimension with the new one
ds = ds.assign_coords(time=time_new)

#Define the dimensions
time_dim = 540  # Number of time steps 1979-01 to 2023-12
j_dim = 120     # j dimension size
i_dim = 360     # i dimension size

#Flatten the lon and lat arrays for the interpolation step
lon_flat = ds['lon_scaler'].values.flatten()
lat_flat = ds['lat_scaler'].values.flatten()

#Create a 2D mesh grid for the target lat/lon grid
lon_new = np.linspace(lon_flat.min(), lon_flat.max(), j_dim)
lat_new = np.linspace(lat_flat.min(), lat_flat.max(), i_dim)
lon_grid, lat_grid = np.meshgrid(lon_new, lat_new)

#Initialize an empty array for the interpolated thickness data
thick_interp = np.empty((time_dim, i_dim, j_dim))

#Perform the interpolation for each time step
thick_da=ds.where(ds<9999.9) #replacing the placeholder of nan values to nan instead of 9999.9
for t in range(time_dim):
    thick_flat = thick_da.heff.isel(time=t).values.flatten()
    thick_interp[t, :, :] = griddata(
        (lon_flat, lat_flat), thick_flat, (lon_grid, lat_grid), method='linear')

#Create the final Dataset with the new dimensions
ds_final = xr.Dataset(
    {
        'sithick': (['time', 'lat', 'lon'], thick_interp)
    },
    coords={
        'time': ds.time,
        'lat': lat_new,
        'lon': lon_new
    }
)

ds_final=ds_final.interpolate_na(dim='lat', method='nearest').interpolate_na(dim='lon', method='nearest')

#ds_final.to_netcdf('heff_10.nc')
print('====')
print(ds_final)
print('====')

lon_min, lon_max =193, 343 #73W & 45W
lat_min, lat_max =14,89.97
#lon_min, lon_max =287, 315 #73W & 45W
#lat_min, lat_max =51,69

# Create a mask for Labrador coast
mask_final = ((ds_final.lat >= lat_min) & (ds_final.lat <= lat_max) &
              (ds_final.lon >= lon_min) & (ds_final.lon <= lon_max))
ds_final_region=ds_final.where(mask_final, drop=True)
ds_final_region.to_netcdf(path+'PIOMAS_sithick_can.nc')
print('saved')
print(ds_final_region)

end_time=time.time()
elapsed_time = end_time - start_time
# Convert seconds to hours, minutes, seconds
hours, remainder = divmod(elapsed_time, 3600)
minutes, seconds = divmod(remainder, 60)

print("Execution time: ", hours, "hours,", minutes, "minutes,", seconds, "seconds")



