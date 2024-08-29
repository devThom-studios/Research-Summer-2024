import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as colors

# File paths
cmip6_path = "/gpfs/fs7/eccc/cccs/kth097/SIT_data/CMIP6/sithick_can/percentiles/"
piomas_path = "/gpfs/fs7/eccc/cccs/kth097/SIT_data/PIOMAS/"
c3s_path = "/gpfs/fs7/eccc/cccs/kth097/SIT_data/copernicus_marine/"

# Opening data
data_10_ssp126 = xr.open_dataset(cmip6_path + "sithick_hist_ssp126_10-p.nc")
data_50_ssp126 = xr.open_dataset(cmip6_path + "sithick_hist_ssp126_50-p.nc")
data_90_ssp126 = xr.open_dataset(cmip6_path + "sithick_hist_ssp126_90-p.nc")

# Observed data
data_piomas = xr.open_dataset(piomas_path + "PIOMAS_sithick_interpolated.nc")
data_c3s = xr.open_dataset(c3s_path + "c3s_sithick_interpolated.nc")

# Selecting data for 1982-2014 (PIOMAS) and 2003-2014 (C3S) for SSP126
mean_data_10_ssp126_1982_2014 = data_10_ssp126["sithick"].sel(time=slice("1982", "2014")).mean(dim="time")
mean_data_50_ssp126_1982_2014 = data_50_ssp126["sithick"].sel(time=slice("1982", "2014")).mean(dim="time")
mean_data_90_ssp126_1982_2014 = data_90_ssp126["sithick"].sel(time=slice("1982", "2014")).mean(dim="time")

mean_data_10_ssp126_2003_2014 = data_10_ssp126["sithick"].sel(time=slice("2003", "2014")).mean(dim="time")
mean_data_50_ssp126_2003_2014 = data_50_ssp126["sithick"].sel(time=slice("2003", "2014")).mean(dim="time")
mean_data_90_ssp126_2003_2014 = data_90_ssp126["sithick"].sel(time=slice("2003", "2014")).mean(dim="time")

mean_data_piomas_1982_2014 = data_piomas["sithick"].sel(time=slice("1982", "2014")).mean(dim="time")
mean_data_c3s_2003_2014 = data_c3s["sea_ice_thickness"].sel(time=slice("2003", "2014")).mean(dim="time")

# Bias calculations
bias_data_10_ssp126_piomas = mean_data_10_ssp126_1982_2014 - mean_data_piomas_1982_2014
bias_data_10_ssp126_c3s = mean_data_10_ssp126_2003_2014 - mean_data_c3s_2003_2014
bias_data_50_ssp126_piomas = mean_data_50_ssp126_1982_2014 - mean_data_piomas_1982_2014
bias_data_50_ssp126_c3s = mean_data_50_ssp126_2003_2014 - mean_data_c3s_2003_2014
bias_data_90_ssp126_piomas = mean_data_90_ssp126_1982_2014 - mean_data_piomas_1982_2014
bias_data_90_ssp126_c3s = mean_data_90_ssp126_2003_2014 - mean_data_c3s_2003_2014

# Calculate percentage biases
def calculate_percent_bias(bias_data, obs_data):
    return (bias_data/obs_data)*100

percent_bias_data_10_piomas = calculate_percent_bias(bias_data_10_ssp126_piomas, mean_data_piomas_1982_2014)
percent_bias_data_10_c3s = calculate_percent_bias(bias_data_10_ssp126_c3s, mean_data_c3s_2003_2014)
percent_bias_data_50_piomas = calculate_percent_bias(bias_data_50_ssp126_piomas, mean_data_piomas_1982_2014)
percent_bias_data_50_c3s = calculate_percent_bias(bias_data_50_ssp126_c3s, mean_data_c3s_2003_2014)
percent_bias_data_90_piomas = calculate_percent_bias(bias_data_90_ssp126_piomas, mean_data_piomas_1982_2014)
percent_bias_data_90_c3s = calculate_percent_bias(bias_data_90_ssp126_c3s, mean_data_c3s_2003_2014)



def plot_sithick_and_bias(data, titles, file_name):
    fig, axs = plt.subplots(2, 2, subplot_kw={'projection': ccrs.RotatedPole(pole_longitude=83, pole_latitude=42.5)}, 
                            figsize=(8, 5))

    norm_first_row = colors.Normalize(vmin=0.1, vmax=4)
    norm_second_row = colors.Normalize(vmin=-50, vmax=50)

    for i, ax in enumerate(axs.flat):
        if i // 2 == 0:
            cmap = plt.get_cmap('viridis', 15)
            contour = ax.pcolormesh(data[i].lon, data[i].lat, data[i],
                                    cmap=cmap, norm=norm_first_row, transform=ccrs.PlateCarree())
        else:
            cmap = plt.get_cmap('bwr', 15)
            contour = ax.pcolormesh(data[i].lon, data[i].lat, data[i],
                                    cmap=cmap, norm=norm_second_row, transform=ccrs.PlateCarree())

        ax.set_extent([-150, -50, 40, 89.97], crs=ccrs.PlateCarree())
        ax.coastlines(zorder=2, linewidth=0.3)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.add_feature(cfeature.LAND, zorder=2)
        ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.3, zorder=2)
        ax.add_feature(cfeature.RIVERS.with_scale('110m'), zorder=2)
        ax.set_title(titles[i], fontsize=8)

    # Add colorbars
    cbar_ax1 = fig.add_axes([0.86, 0.54, 0.02, 0.34])
    cbar_ax2 = fig.add_axes([0.86, 0.11, 0.02, 0.34])

    ticks1 = np.linspace(0.1, 4.0, 8)
    cbar1 = fig.colorbar(axs[0, 0].collections[0], cax=cbar_ax1)
    cbar1.set_ticks(ticks1)
    cbar1.set_ticklabels(['0.1', '0.7', '1.2', '1.8', '2.3', '2.9', '3.4', '4.0'])
    

    ticks2 = np.linspace(-50, 50, 9)
    cbar2=fig.colorbar(axs[1, 0].collections[0], cax=cbar_ax2)
    cbar2.set_ticks(ticks2)
    cbar2.set_ticklabels([f'{tick:.2f}' for tick in ticks2])

    plt.subplots_adjust(wspace=-0.3, hspace=0.28)
    plt.savefig('/home/kth097/scripts/python_script/new_figures/'+file_name, dpi=500, bbox_inches='tight')
   # plt.show()


# Titles for each plot
titles_10 = [
    'PIOMAS mean from 1982-2014 (m)',
    'C3S mean from 2003-2014 (m)',
    'Percentage Bias (%):\nCMIP6 10th Percent vs PIOMAS',
    'Percentage Bias (%):\nCMIP6 10th Percent vs C3S',
]

titles_50 = [
    'PIOMAS mean from 1982-2014 (m)',
    'C3S mean from 2003-2014 (m)',
    'Percentage Bias (%):\nCMIP6 50th Percent vs PIOMAS',
    'Percentage Bias (%):\nCMIP6 50th Percent vs C3S',
]


titles_90 = [
    'PIOMAS mean from 1982-2014 (m)',
    'C3S mean from 2003-2014 (m)',
    'Percentage Bias (%):\nCMIP6 90th Percent vs PIOMAS',
    'Percentage Bias (%):\nCMIP6 90th Percent vs C3S',
]



# Plot each percentile
plot_sithick_and_bias([mean_data_piomas_1982_2014.where(mean_data_piomas_1982_2014>=0.02, np.nan), mean_data_c3s_2003_2014, percent_bias_data_10_piomas, percent_bias_data_10_c3s],titles_10, 'sithick_percent_bias_10th.jpg')

plot_sithick_and_bias([mean_data_piomas_1982_2014.where(mean_data_piomas_1982_2014>=0.02, np.nan), mean_data_c3s_2003_2014, percent_bias_data_50_piomas, percent_bias_data_50_c3s], titles_50, 'sithick_percent_bias_50th.jpg')

plot_sithick_and_bias([mean_data_piomas_1982_2014.where(mean_data_piomas_1982_2014>=0.02, np.nan), mean_data_c3s_2003_2014, percent_bias_data_90_piomas, percent_bias_data_90_c3s], titles_90, 'sithick_percent_bias_90th.jpg')
