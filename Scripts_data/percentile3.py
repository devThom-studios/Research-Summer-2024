import xarray as xr
import numpy as np
import pandas as pd
import glob
import time


path="/gpfs/fs7/eccc/cccs/kth097/SIT_data/CMIP6/sithick_can/hist+ssp/"
path1="/gpfs/fs7/eccc/cccs/kth097/SIT_data/CMIP6/sithick_can/percentiles/"

scenarios=['ssp126, ssp245, ssp370, ssp585']
scenarios=['ssp585']
start_time = time.time()
new_time = pd.date_range('1900-01-01', '2100-12-01', freq='MS')  # Monthly start frequency
for scenario in scenarios:
    file_pattern=glob.glob(path+"sithick_SImon*+"+scenario+"_r1i1p1f1_gn_1900-2100_can.nc")
    datasets = []
    for file in sorted(file_pattern):
        dataset = xr.open_dataset(file)
        # Replacing the time coordinates with the new time range
        dataset['time'] = new_time[:dataset['time'].size]
        if 'time_bnds' in dataset:
            data = dataset.drop_vars('time_bnds')
        datasets.append(data)
    combined_data = xr.concat(datasets, dim='model')

    #calculating the percentiles
    siconc_10 = combined_data.quantile(0.1, dim='model')
    siconc_50 = combined_data.quantile(0.5, dim='model')
    siconc_90 = combined_data.quantile(0.9, dim='model')

    siconc_10.to_netcdf(path1+"sithick_hist_"+scenario+"_10-p.nc")
    siconc_50.to_netcdf(path1+"sithick_hist_"+scenario+"_50-p.nc")
    siconc_90.to_netcdf(path1+"sithick_hist_"+scenario+"_90-p.nc")

    print(scenario+" completed..")

    # Record the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
print("Done")



