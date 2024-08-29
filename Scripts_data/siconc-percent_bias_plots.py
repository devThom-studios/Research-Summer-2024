import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.colors as colors

# File paths
cmip6_path = "/gpfs/fs7/eccc/cccs/kth097/SIC_data/CMIP6/percentiles/"
hadisst_path = "/gpfs/fs7/eccc/cccs/kth097/SIC_data/HadISST/"
ostia_path = "/gpfs/fs7/eccc/cccs/kth097/SIC_data/OSTIA_copernicus/"

# Opening data
data_10_ssp126 = xr.open_dataset(cmip6_path + "siconc_hist_ssp126_10-p.nc")
data_50_ssp126 = xr.open_dataset(cmip6_path + "siconc_hist_ssp126_50-p.nc")
data_90_ssp126 = xr.open_dataset(cmip6_path + "siconc_hist_ssp126_90-p.nc")

# Observed data
data_hadisst = xr.open_dataset(hadisst_path + "HadISST_siconc_interpolated.nc") * 100
data_ostia = xr.open_dataset(ostia_path + "OSTIA_siconc_interpolated.nc") * 100

# Select and calculate means for the 1982-2014 period
def calculate_mean(data, varname, time_slice):
    return data[varname].sel(time=slice(time_slice[0], time_slice[1])).mean(dim="time")

time_slice = ("1982", "2014")
mean_data_10_ssp126 = calculate_mean(data_10_ssp126, "siconc", time_slice)
mean_data_50_ssp126 = calculate_mean(data_50_ssp126, "siconc", time_slice)
mean_data_90_ssp126 = calculate_mean(data_90_ssp126, "siconc", time_slice)
mean_data_hadisst = calculate_mean(data_hadisst, "sic", time_slice)
mean_data_ostia = calculate_mean(data_ostia, "sea_ice_fraction", time_slice)

# Calculate biases
def calculate_bias(model_data, obs_data):
    return model_data - obs_data

bias_data_10_hadisst = calculate_bias(mean_data_10_ssp126, mean_data_hadisst)
bias_data_10_ostia = calculate_bias(mean_data_10_ssp126, mean_data_ostia)
bias_data_50_hadisst = calculate_bias(mean_data_50_ssp126, mean_data_hadisst)
bias_data_50_ostia = calculate_bias(mean_data_50_ssp126, mean_data_ostia)
bias_data_90_hadisst = calculate_bias(mean_data_90_ssp126, mean_data_hadisst)
bias_data_90_ostia = calculate_bias(mean_data_90_ssp126, mean_data_ostia)


# Calculate percentage biases
def calculate_percent_bias(bias_data, obs_data):
    return (bias_data/obs_data)*100

percent_bias_data_10_hadisst = calculate_percent_bias(bias_data_10_hadisst, mean_data_hadisst)
percent_bias_data_10_ostia = calculate_percent_bias(bias_data_10_ostia, mean_data_ostia)
percent_bias_data_50_hadisst = calculate_percent_bias(bias_data_50_hadisst, mean_data_hadisst)
percent_bias_data_50_ostia = calculate_percent_bias(bias_data_50_ostia, mean_data_ostia)
percent_bias_data_90_hadisst = calculate_percent_bias(bias_data_90_hadisst, mean_data_hadisst)
percent_bias_data_90_ostia = calculate_percent_bias(bias_data_90_ostia, mean_data_ostia)


# Plotting function
def plot_sic_and_bias(data, titles, file_name):
    fig, axs = plt.subplots(2, 2, subplot_kw={'projection': ccrs.RotatedPole(pole_longitude=83, pole_latitude=42.5)}, 
            figsize=(8, 5))

    norm_first_row = colors.Normalize(vmin=0.2, vmax=100)
    norm_second_row = colors.Normalize(vmin=-50, vmax=50)

    for i, ax in enumerate(axs.flat):
        if i < 2:
            cmap = plt.get_cmap('viridis', 15)
            norm = norm_first_row
            contour = ax.contourf(data[i].lon, data[i].lat, data[i],
                                  cmap=cmap, norm=norm, levels=np.linspace(0.2, 100, 15),
                                  transform=ccrs.PlateCarree())
        else:
            cmap = plt.get_cmap('bwr', 15)
            norm = norm_second_row
            contour = ax.pcolormesh(data[i].lon, data[i].lat, data[i], 
                                     cmap=cmap, norm=norm, transform=ccrs.PlateCarree())

        ax.set_extent([-150, -50, 40, 89.97], crs=ccrs.PlateCarree())    
        ax.coastlines(zorder=2, linewidth=0.3)
        ax.add_feature(cfeature.BORDERS, linewidth=0.3)
        ax.add_feature(cfeature.LAND, zorder=2)
        ax.add_feature(cfeature.STATES.with_scale('10m'), linewidth=0.3, zorder=2)
        ax.add_feature(cfeature.RIVERS.with_scale('110m'), zorder=2)
        ax.set_title(titles[i], fontsize=8)

    ticks = np.linspace(-50, 50, 9)

    # Add colorbars
    cbar_ax1 = fig.add_axes([0.86, 0.54, 0.02, 0.34])
    cbar_ax2 = fig.add_axes([0.86, 0.11, 0.02, 0.34])
    fig.colorbar(axs[0, 0].collections[0], cax=cbar_ax1)
    cbar2=fig.colorbar(axs[1, 0].collections[0], cax=cbar_ax2)
    cbar2.set_ticks(ticks)
    cbar2.set_ticklabels([f'{tick:.2f}' for tick in ticks])

    # Adjust layout to make subplots more square-like
    plt.subplots_adjust(wspace=-0.3, hspace=0.28)
    plt.savefig('/home/kth097/scripts/python_script/new_figures/'+file_name, dpi=500, bbox_inches='tight')
    plt.show()

# Titles for each percentile
titles_10 = [
    'HadISST mean from 1982-2014 (%)',
    'OSTIA mean from 1982-2014 (%)',
    'Percentage Bias (%):\nCMIP6 10th Percent vs HadISST',
    'Percentage Bias (%):\nCMIP6 10th Percent vs OSTIA',
]

titles_50 = [
    'HadISST mean from 1982-2014 (%)',
    'OSTIA mean from 1982-2014 (%)',
    'Percentage Bias (%):\nCMIP6 50th Percent vs HadISST',
    'Percentage Bias (%):\nCMIP6 50th Percent vs OSTIA',
]

titles_90 = [
    'HadISST mean from 1982-2014 (%)',
    'OSTIA mean from 1982-2014 (%)',
    'Percentage Bias (%):\nCMIP6 90th Percent vs HadISST',
    'Percentage Bias (%):\nCMIP6 90th Percent vs OSTIA',
]


# Plot each percentile
plot_sic_and_bias([mean_data_hadisst, mean_data_ostia, percent_bias_data_10_hadisst, percent_bias_data_10_ostia], 
                   titles_10, 'siconc_percent_bias_10th.jpg')
plot_sic_and_bias([mean_data_hadisst, mean_data_ostia, percent_bias_data_50_hadisst, percent_bias_data_50_ostia], 
                   titles_50, 'siconc_percent_bias_50th.jpg')
plot_sic_and_bias([mean_data_hadisst, mean_data_ostia, percent_bias_data_90_hadisst, percent_bias_data_90_ostia], 
                   titles_90, 'siconc_percent_bias_90th.jpg')

