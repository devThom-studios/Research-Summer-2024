import xarray as xr
import glob
import pandas as pd
import numpy as np

path = "/gpfs/fs7/eccc/cccs/kth097/SIT_data/CMIP6/sithick_can/"
path2 ="/gpfs/fs7/eccc/cccs/kth097/SIT_data/CMIP6/sithick_can/hist+ssp/"

models = ['AWI-CM-1-1-MR', 'CESM2-WACCM', 'CMCC-CM2-SR5', 'CMCC-ESM2', 'CanESM5', 
          'EC-Earth3_', 'EC-Earth3-Veg_', 'EC-Earth3-Veg-LR_', 'IPSL-CM6A-LR', 
          'KACE-1-0-G', 'MIROC6', 'MPI-ESM1-2-LR', 'MPI-ESM1-2-HR', 'MRI-ESM2-0', 
          'NorESM2-LM', 'NorESM2-MM']

# For testing, use only the models needed
#models = ['EC-Earth3_']
#models = ['CMCC-CM2-SR5', 'CMCC-ESM2', 'EC-Earth3', 'EC-Earth3-Veg', 'EC-Earth3-Veg-LR']
new_time = pd.date_range('1900-01-01', '2100-12-01', freq='MS')

# Looping through each model
for model in models:
    file_pattern = sorted(glob.glob(path + '*' + model + '*'))
    print(file_pattern)
    
    if len(file_pattern) < 2:
        print(f"Not enough files found for model {model}")
        continue
    
    try:
        data_histor = xr.open_dataset(file_pattern[0])
        data_ssp126 = xr.open_dataset(file_pattern[1])
        data_ssp245 = xr.open_dataset(file_pattern[2])
        data_ssp370 = xr.open_dataset(file_pattern[3])
        data_ssp585 = xr.open_dataset(file_pattern[4])

        data1 = data_histor.sel(time=slice('1900-01-01', '2014-12-31'))
        data2 = data_ssp126.sel(time=slice('2015-01-01', '2100-12-31'))
        data3 = data_ssp245.sel(time=slice('2015-01-01', '2100-12-31'))
        data4 = data_ssp370.sel(time=slice('2015-01-01', '2100-12-31'))
        data5 = data_ssp585.sel(time=slice('2015-01-01', '2100-12-31'))

        # Combine or further process your data here
        
        combined_data_hist_ssp126 = xr.concat([data1,data2], dim='time')
        combined_data_hist_ssp245 = xr.concat([data1,data3], dim='time')
        combined_data_hist_ssp370 = xr.concat([data1,data4], dim='time')
        combined_data_hist_ssp585 = xr.concat([data1,data5], dim='time')

        #saving file
        combined_data_hist_ssp126.to_netcdf(path2+'sithick_SImon_'+model+'_historical+ssp126_r1i1p1f1_gn_1900-2100_can.nc')
        combined_data_hist_ssp245.to_netcdf(path2+'sithick_SImon_'+model+'_historical+ssp245_r1i1p1f1_gn_1900-2100_can.nc')
        combined_data_hist_ssp370.to_netcdf(path2+'sithick_SImon_'+model+'_historical+ssp370_r1i1p1f1_gn_1900-2100_can.nc')
        combined_data_hist_ssp585.to_netcdf(path2+'sithick_SImon_'+model+'_historical+ssp585_r1i1p1f1_gn_1900-2100_can.nc')


    except Exception as e:
        print(f"Error processing model {model}: {e}")


    print(model + " completed...")
