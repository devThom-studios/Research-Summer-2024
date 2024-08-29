import xarray as xr
import numpy as np

input_dir="/gpfs/fs7/eccc/cccs/kth097/SIT_data/PIOMAS/all_heff_corrected_coordinates.nc"
output_dir="/gpfs/fs7/eccc/cccs/kth097/SIT_data/PIOMAS/all_heff_corrected_coordinates_can.nc"

print('file opening')
data = xr.open_dataset(input_dir)

# selecting sic variable
print('selecting variable')
sic_=data['heff']
sic=sic_.where(sic_<=10, np.nan)
# selecting lon lat
minimum_longitude=-167
maximum_longitude=-17
minimum_latitude=14
maximum_latitude=89.97

sic_canada=sic.sel(lat=slice(minimum_latitude, maximum_latitude),
                   lon=slice(minimum_longitude, maximum_longitude))

# Saving to a new file
sic_canada.to_netcdf(path=output_dir)

print(sic_canada)
print ("completed.")
