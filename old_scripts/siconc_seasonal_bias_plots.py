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
data_oisst = xr.open_dataset(oisst_path+"OISST_siconc_interpolated.nc").isel(zlev=0)*100

# selecting var sea ice concentration for 1982 to 2014 for ssp126
data_10_ssp126_1982_2014=data_10_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_50_ssp126_1982_2014=data_50_ssp126["siconc"].sel(time=slice("1982", "2014"))
data_90_ssp126_1982_2014=data_90_ssp126["siconc"].sel(time=slice("1982", "2014"))

# mean
seasonal_data_10_ssp126_1982_2014=data_10_ssp126_1982_2014.groupby('time.season').mean(dim="time")
seasonal_data_50_ssp126_1982_2014=data_50_ssp126_1982_2014.groupby('time.season').mean(dim="time")
#seasonal_data_90_ssp126_1982_2014=data_90_ssp126_1982_2014.groupby('time.season').mean(dim="time")


# selecting var sea ice concentration for 1982 to 2014 for observed data/ resampling into monthly
data_hadisst_1982_2014=data_hadisst["sic"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
data_ostia_1982_2014=data_ostia["sea_ice_fraction"].resample(time="MS").mean().sel(time=slice("1982", "2014"))
#data_oisst_1982_2014=data_oisst["ice"].resample(time="MS").mean().sel(time=slice("1982", "2014"))

# mean
seasonal_data_hadisst_1982_2014=data_hadisst_1982_2014.groupby('time.season').mean(dim="time")
seasonal_data_ostia_1982_2014=data_ostia_1982_2014.groupby('time.season').mean(dim="time")
#seasonal_data_oisst_1982_2014=data_oisst_1982_2014.groupby('time.season').mean(dim="time")


# bias (difference between model and observed)
bias_data_10_ssp126_hadisst=seasonal_data_10_ssp126_1982_2014-seasonal_data_hadisst_1982_2014
bias_data_10_ssp126_ostia=seasonal_data_10_ssp126_1982_2014-seasonal_data_ostia_1982_2014
#bias_data_10_ssp126_oisst=seasonal_data_10_ssp126_1982_2014-seasonal_data_oisst_1982_2014

#plt.pcolormesh(bias_data_10_ssp126_hadisst.lon, bias_data_10_ssp126_hadisst.lat, bias_data_10_ssp126_hadisst)
#plt.show()

#plotting
data_list=[seasonal_data_hadisst_1982_2014, seasonal_data_ostia_1982_2014,
        bias_data_10_ssp126_hadisst, bias_data_10_ssp126_ostia]


# Create normalization for the colorbars
norm_first_row = colors.Normalize(vmin=0.2, vmax=100)
norm_second_row = colors.Normalize(vmin=-30, vmax=30)

print(data_list[0][0])
# Titles for subplots
titles = [
    'HadISST DJF from 1982-2014 (%)',
    'OSTIA DJF from 1982-2014 (%)',
    'CMIP6 10th percent - HadISST (%)',
    'CMIP6 10th percent - OSTIA (%)',
]

fig, axs = plt.subplots(2, 2, subplot_kw={'projection': ccrs.RotatedPole(pole_longitude=83, pole_latitude=42.5)}, figsize=(8, 5))


# Plot each dataset in the list
for i, ax in enumerate(axs.flat):
    # Set the colormap and normalization based on the row index
    if i // 2 == 0:
        cmap = plt.get_cmap('viridis', 15)
        norm = norm_first_row
        contour1 = ax.contourf(data_list[i].lon, data_list[i].lat, data_list[i][0],
            cmap=cmap,norm=norm,vmin=0.2,vmax=100, levels=np.round(np.linspace(0.2, 100, 15),1),
            transform=ccrs.PlateCarree())

    else:
        cmap = plt.get_cmap('coolwarm', 15)
        norm = norm_second_row
        #contour2 = ax.contourf(data_list[i].lon, data_list[i].lat, data_list[i][2],
        #cmap=cmap, norm=norm, vmin=-105,vmax=105, levels=np.round(np.linspace(0, 100, 15),1),
        #transform=ccrs.PlateCarree())
        contour2 = ax.pcolormesh(data_list[i].lon, data_list[i].lat, data_list[i][0],
                cmap=cmap, norm=norm,
                transform=ccrs.PlateCarree())


    ax.set_extent([-150, -50, 40, 89.97], crs=ccrs.PlateCarree())
    ax.coastlines(zorder=2, linewidth=0.3)
    ax.add_feature(cfeature.BORDERS, linewidth=0.3)
    ax.add_feature(cfeature.LAND, zorder=2)
    ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.3, zorder=2)
    ax.add_feature(cfeature.RIVERS.with_scale('110m'), zorder=2)
    ax.set_title(titles[i], fontsize=8)

# Add colorbars for each row
cbar_ax1 = fig.add_axes([0.86, 0.54, 0.02, 0.34])  # Adjust these values as needed
cbar_ax2 = fig.add_axes([0.86, 0.11, 0.02, 0.34])  # Adjust these values as needed

# Plot the color bars
cbar1 = fig.colorbar(contour1, cax=cbar_ax1, orientation='vertical')
cbar2 = fig.colorbar(contour2, cax=cbar_ax2, orientation='vertical')

# Adjust layout to make subplots more square-like
plt.subplots_adjust(wspace=-0.3, hspace=0.28)

# Save plot to file and display
plt.savefig('siconc_DJF_bias_10-p.jpg', dpi=500, bbox_inches='tight')
plt.show()

