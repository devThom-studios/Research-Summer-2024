import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as colors

cmip6_path="/gpfs/fs7/eccc/cccs/kth097/SIT_data/CMIP6/sithick_can/percentiles/"
piomas_path="/gpfs/fs7/eccc/cccs/kth097/SIT_data/PIOMAS/"
c3s_path="/gpfs/fs7/eccc/cccs/kth097/SIT_data/copernicus_marine/"

#opening data
data_10_ssp126 = xr.open_dataset(cmip6_path+"sithick_hist_ssp126_10-p.nc")
data_50_ssp126 = xr.open_dataset(cmip6_path+"sithick_hist_ssp126_50-p.nc")
data_90_ssp126 = xr.open_dataset(cmip6_path+"sithick_hist_ssp126_90-p.nc")

# observed data
data_piomas = xr.open_dataset(piomas_path+"PIOMAS_sithick_interpolated.nc")
data_c3s = xr.open_dataset(c3s_path+"c3s_sithick_interpolated.nc")

# selecting var sea ice concentration for 1982 to 2014 for ssp126
data_10_ssp126_1982_2014=data_10_ssp126["sithick"].sel(time=slice("1982", "2014"))
data_50_ssp126_1982_2014=data_50_ssp126["sithick"].sel(time=slice("1982", "2014"))
data_90_ssp126_1982_2014=data_90_ssp126["sithick"].sel(time=slice("1982", "2014"))


data_10_ssp126_2003_2014=data_10_ssp126["sithick"].sel(time=slice("2003", "2014"))
data_50_ssp126_2003_2014=data_50_ssp126["sithick"].sel(time=slice("2003", "2014"))
data_90_ssp126_2003_2014=data_90_ssp126["sithick"].sel(time=slice("2003", "2014"))

# mean
seasonal_data_10_ssp126_1982_2014=data_10_ssp126_1982_2014.groupby('time.season').mean(dim="time")
seasonal_data_50_ssp126_1982_2014=data_50_ssp126_1982_2014.groupby('time.season').mean(dim="time")
seasonal_data_90_ssp126_1982_2014=data_90_ssp126_1982_2014.groupby('time.season').mean(dim="time")

seasonal_data_10_ssp126_2003_2014=data_10_ssp126_2003_2014.groupby('time.season').mean(dim="time")
seasonal_data_50_ssp126_2003_2014=data_50_ssp126_2003_2014.groupby('time.season').mean(dim="time")
seasonal_data_90_ssp126_2003_2014=data_90_ssp126_2003_2014.groupby('time.season').mean(dim="time")


# selecting var sea ice concentration for 1982 to 2014 for observed data/ resampling into monthly
data_piomas_1982_2014=data_piomas["sithick"].sel(time=slice("1982", "2014"))
data_c3s_2003_2014=data_c3s["sea_ice_thickness"].sel(time=slice("2003", "2014"))

# mean
seasonal_data_piomas_1982_2014=data_piomas_1982_2014.groupby('time.season').mean(dim="time")
seasonal_data_c3s_2003_2014=data_c3s_2003_2014.groupby('time.season').mean(dim="time")


# bias (difference between model and observed)
bias_data_10_ssp126_piomas=seasonal_data_90_ssp126_1982_2014-seasonal_data_piomas_1982_2014
bias_data_10_ssp126_c3s=seasonal_data_90_ssp126_2003_2014-seasonal_data_c3s_2003_2014.fillna(0)

#plotting
data_list=[seasonal_data_piomas_1982_2014.fillna(0), seasonal_data_c3s_2003_2014.fillna(0), bias_data_10_ssp126_piomas.fillna(0), bias_data_10_ssp126_c3s.fillna(0)]

# Create normalization for the colorbars
norm_first_row = colors.Normalize(vmin=0, vmax=4)
norm_second_row = colors.Normalize(vmin=-4, vmax=4)

print(data_list[1][3])

# Titles for subplots
titles = [
    'PIOMAS SON from 1982-2014 (m)',
    'C3S SON from 2003-2014 (m)',
    'CMIP6 90th percent - PIOMAS (m)',
    'CMIP6 90th percent - C3S (m)',
]

fig, axs = plt.subplots(2, 2, subplot_kw={'projection': ccrs.RotatedPole(pole_longitude=83, pole_latitude=42.5)}, figsize=(8, 5))


# Plot each dataset in the list
for i, ax in enumerate(axs.flat):
    # Set the colormap and normalization based on the row index
    if i // 2 == 0:
        cmap = plt.get_cmap('viridis', 15)
        contour1 = ax.pcolormesh(data_list[i].lon, data_list[i].lat, data_list[i][3],
            cmap=cmap,  norm=norm_first_row,
            transform=ccrs.PlateCarree())

    else:
        cmap = plt.get_cmap('coolwarm', 15)
        contour2 = ax.pcolormesh(data_list[i].lon, data_list[i].lat, data_list[i][3],
                cmap=cmap, norm=norm_second_row,
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
plt.savefig('sithick_SON_bias_90-p.jpg', dpi=500, bbox_inches='tight')
plt.show()

