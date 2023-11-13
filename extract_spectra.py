import earthaccess
auth = earthaccess.login(persist=True)

#imports
import s3fs
import xarray as xr
import hvplot.xarray
import holoviews as hv
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import netCDF4 as nc
import json
import geopandas as gpd

#our modules
from utils.emit_tools import emit_xarray, quality_mask, gamma_adjust
from utils.synthmix import extract_points, mix_fast
from utils.s3_access import get_temp_creds


temp_creds_req = get_temp_creds()
#these are our files - the s3 links

f_url = ['s3://lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20230119T114235_2301907_004/EMIT_L2A_RFL_001_20230119T114235_2301907_004.nc',
         's3://lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20230115T132032_2301508_014/EMIT_L2A_RFL_001_20230115T132032_2301508_014.nc',
        's3://lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20230119T114247_2301907_005/EMIT_L2A_RFL_001_20230119T114247_2301907_005.nc']

f_mask_url = ['s3://lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20230119T114235_2301907_004/EMIT_L2A_MASK_001_20230119T114235_2301907_004.nc',
         's3://lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20230115T132032_2301508_014/EMIT_L2A_MASK_001_20230115T132032_2301508_014.nc',
        's3://lp-prod-protected/EMITL2ARFL.001/EMIT_L2A_RFL_001_20230119T114247_2301907_005/EMIT_L2A_MASK_001_20230119T114247_2301907_005.nc']

final_df = pd.DataFrame()
# Pass Authentication to s3fs
fs_s3 = s3fs.S3FileSystem(anon=False, 
                          key=temp_creds_req['accessKeyId'], 
                          secret=temp_creds_req['secretAccessKey'], 
                          token=temp_creds_req['sessionToken'])

for i in range(3):
    print('starting')
    # Open s3 url
    fp = fs_s3.open(f_url[i], mode='rb')
    fp_mask = fs_s3.open(f_mask_url[i], mode='rb')

    # Open dataset with xarray
    ds = xr.open_dataset(fp,engine='h5netcdf',chunks='auto')

    #mask
    flags=[7]
    mask = quality_mask(fp_mask,flags)

    #load data
    ds = emit_xarray(fp, ortho=True,qmask=mask)
    ds = ds.chunk({'latitude':-1,'longitude':-1,'wavelengths':1})
    ds = ds.where(ds.good_wavelengths.compute()==1,drop=True)

    #load points
    #load points
    gdf = gpd.read_file("data/emit_unmix.gpkg")
    #add x and y locations as df columns
    gdf['Longitude'] = gdf.centroid.x
    gdf['Latitude'] = gdf.centroid.y
    #drops cols we dont need
    df = pd.DataFrame(gdf).drop(['geometry','ID'],axis=1)
    #add id col
    df['ID'] = df.index

    #extract
    df = extract_points(df,ds)
    
    final_df = pd.concat([final_df,df], ignore_index=True)
    
    print('ending')

final_df = final_df.dropna(subset=['reflectance'])
csv_file_path = 'data/df_cleaned.csv'
final_df.to_csv(csv_file_path, index=False)