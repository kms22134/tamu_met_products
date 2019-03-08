import logging;
import os, json;
import cartopy.crs as ccrs;
from .plot_utils import add_colorbar, plot_barbs, plot_basemap, baseLabel;
from . import color_maps;


dir = os.path.dirname( os.path.realpath(__file__) );
with open( os.path.join( dir, 'plot_opts.json' ), 'r' ) as fid:
  opts = json.load(fid);

################################################################################
def plot_850hPa_temp_hght_barbs( ax, lon, lat, temp, hght, model, initTime, fcstTime, u=None, v=None, **kwargs ):
  '''
  Name:
    plot_850hPa_temp_hght_barbs
  Purpose:
    A python function to plot a 850 hPa plot like the one in the
    lower left of the HDWX 4-panel plot
  Inputs:
    ax       : Axis to plot on
    lon      : Longitude values for plot
    lat      : Latitude values for plot
    temp     : temperature at 850 hPa to plot
    hght     : Geopotential heights at 850 hPa to plot
    model    : Name of the model being plotted
    initTime : Initialization time of the model run
    fcstTime : Forecast time of the model run
  Keywords:
    u : u-wind components for wind barbs
    v : v-wind components for wind barbs
  Outputs:
    Returns the filled contour, contour, and colorbar objects
  '''
  log = logging.getLogger(__name__)
  log.info('Creating 850 hPa plot')
  projection = kwargs.pop( 'projection', ccrs.PlateCarree() );                  # Get default data projection

  xyz = ax.projection.transform_points(projection, lon.m, lat.m);               # Project longitude/latitude to map; cuts down on projecting multiple times
  xx  = xyz[:,:,0];                                                             # Get re-projected longitudes
  yy  = xyz[:,:,1];                                                             # Get re-projected latitudes

  ax, scale = plot_basemap(ax);                                                 # Set up the basemap, get updated axis and map scale
  log.info('Plotting surface temperature')

  cf = ax.contourf(xx, yy, temp.to('degC'), 
                      cmap      = color_maps.temp_850['cmap'], 
                      norm      = color_maps.temp_850['norm'],
                      levels    = color_maps.temp_850['lvls'],
                      **opts['contourf_Opts'])

  c1 = ax.contour(xx, yy, temp.to('degC'), 
         levels = 0, colors = (0,0,1), linewidths = 2);                         # Contour for 0 degree C line

  plot_barbs( ax, scale, xx, yy, u, v );                                        # Plot wind barbs

  log.debug('Plotting geopotential height')
  c2 = ax.contour(xx, yy, hght, **opts['contour_Opts']);                        # Contour the geopotential height
  ax.clabel(c2, **opts['clabel_Opts']);                                         # Change contour label settings
  cbar = add_colorbar( cf, ax, color_maps.temp_850['lvls'], **kwargs );         # Add colorbar

  txt = baseLabel( model, initTime, fcstTime );                                 # Get base string for label
  txt.append('850-hPa HEIGHTS, WINDS, TEMP (C)');                               # Update label
  t = ax.text(0.5, 0, '\n'.join( txt ),
                 verticalalignment   = 'top', 
                 horizontalalignment = 'center',
                 transform           = ax.transAxes)                            # Add label to axes

  return cf, c2, cbar