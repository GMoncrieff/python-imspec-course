from utils.s3_access import get_temp_creds
temp_creds_req = get_temp_creds()

import argparse
import logging
import s3fs
import xarray as xr
import rioxarray as riox
import pandas as pd
import numpy as np
import os
import json
from einops import rearrange
from xgboost import XGBRegressor

from dask.distributed import Client, LocalCluster, progress

#our modules
from utils.emit_tools import emit_xarray, quality_mask, ortho_xr

#get xgb model
def get_xgb_model():
    model = XGBRegressor()
    model.load_model('models/best_xgb_model.json')
    return model

#predict on chunks
def pred_chunk(arr,fmodel):
    #fill nas
    arr = arr[:,:,:-1]
    xs, ys, zs = arr.shape
    arr = rearrange(arr,'x y z -> (x y) z')
    arr=np.nan_to_num(arr)
    #predict
    ypred = fmodel.result().predict(arr)
    #clip to 0-100
    ypred = np.clip(ypred,0,100)
    ypred = rearrange(ypred,'(x y) z -> x y z', x=xs,y=ys)
    return ypred

if __name__ == "__main__":
    #argparser to get file paths
    parser = argparse.ArgumentParser()
    parser.add_argument('--f_url', type=str, required=True, help='EMIT file s3 url')
    parser.add_argument('--f_mask_url', type=str, required=True, help='EMIT mask s3 url')
    parser.add_argument('--log', type=str, help='Set log level')
    args = parser.parse_args()
    
    #setup logging
    if args.log:
        level = getattr(logging, args.log.upper(), None)
        if not isinstance(level, int):
            raise ValueError(f'Invalid log level: {args.log}')
        logging.basicConfig(level=level)
    
    logging.info('setting up dask distributed scheduler')
    cluster = LocalCluster(n_workers=4)
    client = Client(cluster)
    print(client)
    
    logging.info('connecting to s3 files')
    logging.debug(f'emit file: {args.f_url}')
    logging.debug(f'emit mask: {args.f_mask_url}')
    # Pass Authentication to s3fs
    fs_s3 = s3fs.S3FileSystem(anon=False, 
        key=temp_creds_req['accessKeyId'], 
        secret=temp_creds_req['secretAccessKey'], 
        token=temp_creds_req['sessionToken'])
    fp = fs_s3.open(args.f_url, mode='rb')
    fp_mask = fs_s3.open(args.f_mask_url, mode='rb')
    
    logging.info('create mask')
    flags=[7]
    mask = quality_mask(fp_mask,flags)
    
    logging.info('create emit xarray')
    ds = emit_xarray(fp, 
        ortho=False,
        chunk={'downtrack':100,'crosstrack':100,'wavelengths':-1})
    ds = ds.where(ds.good_wavelengths.compute()==1,drop=True)
    
    logging.info('submit model to client')
    fmodel = client.submit(get_xgb_model)
    
    logging.info('apply model')
    res = xr.apply_ufunc(pred_chunk, #the function
        ds, #the data
        input_core_dims=[['wavelengths']], #the dims we will lose in the result
        exclude_dims=set(('wavelengths',)), #the dims we will lose in the result
        output_core_dims=[["class"]], #the dims we will gain in the result
        dask="parallelized", #use dask
        output_dtypes=[np.uint8], #dtype of result
        output_sizes={"class": 4}, #length of new dim,
        keep_attrs='override',
        kwargs={'fmodel':fmodel}) #addiotnal args to func
    
    logging.info('apply mask result')
    mask = mask[:,:,np.newaxis]
    res = res.where(mask != 1,-9999)
    
    logging.info('compute result')
    res = res.persist()
    progress(res,notebook=False)
    res = res.load()
    
    logging.debug(f'result: {res}')
    
    logging.info('orthorectify result')
    res = ortho_xr(res, GLT_NODATA_VALUE=0, fill_value = -9999)
    
    logging.info('creating geotiff')
    crs = 'epsg:4326'
    logging.debug(f'using crs: {crs}')
    res = res.rio.write_crs(crs)
    #read in class names
    classes = json.load(open("data/classes.json"))
    classes = list(classes.keys())
    res.coords["class"] = classes
    #convert to dataset with one var per class
    res = (res["reflectance"]
            .to_dataset(dim="class")
            .fillna(255) #our values are 0-100 so lets make then int8
            .astype("int8")
          )
    
    logging.info('writing geotiff')
    #get infilename
    filename_with_ext = os.path.basename(args.f_url)
    fullpath = f'data/unmixed/unmixed_{os.path.splitext(filename_with_ext)[0]}.tiff'
    logging.info(f'writing to {fullpath}')
    res.rio.to_raster(fullpath,dtype='int8')
    
    logging.info('success')
    