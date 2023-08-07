import pandas as pd
import numpy as np
import xarray as xr

def extract_points(points,ds):
    # df: points for spectral lib
    #should be comma delim with cols ID (int) ,Category (str),Latitude (dbl),Longitude (dbl)
    #in EPSG 4326 projection
    
    #extract reflectance at points
    points = points.set_index(['ID'])
    xp = points.to_xarray()
    extracted = ds.sel(latitude=xp.Latitude,longitude=xp.Longitude, method='nearest').to_dataframe()
    df = extracted.join(points['Category'], on=['ID'])
    df = df.reset_index()
    df.loc[:]['reflectance'][df.loc[:]['reflectance'] == -0.1] = 0
    df_long = df[['Category','reflectance','wavelengths','ID']]

    df_cat = df_long[['ID', 'Category']].drop_duplicates(subset='ID')

    #convert long to wide df with a column for each wavelength. add column for the category of each point
    df_wide = df_long.pivot(index='ID', columns='wavelengths', values='reflectance')
    df_final = df_cat.set_index('ID').join(df_wide)
    #drop index from df
    df_final.reset_index(inplace=True)
    #drop category column
    df_final.drop(columns=['ID'], inplace=True)
    #fill na
    df_final.fillna(np.nan, inplace=True)
    
    return df

def mix_fast(df,nsamp):
    #df is your dataframe and 'class' is the class label column
    #df = pd.DataFrame({'f1': [1, 2, 3, 4,5,6,7,8], 'f2': [5, 6, 7, 8,9,10,11,12], 'class': [0, 4,0,1,3,2,2,1]})

    num_rows, num_cols = df.shape

    # Create a new dataframe for synthetic data
    df_synthetic = []

    # Calculate class proportions in original dataframe
    all_class = list(df['Category'].unique())

    # Number of synthetic rows you want to create
    num_synthetic_rows = nsamp

    for i in range(num_synthetic_rows):
        nclass = np.random.randint(1, 3)
        selected_rows = np.random.choice(num_rows, size=nclass, replace=False)

        # Generate random weights
        weights = np.random.dirichlet(np.ones(len(selected_rows)))

        # Calculate new row by multiplying weights with selected rows and summing them up
        new_row = df.iloc[selected_rows,:-1].multiply(weights, axis=0).sum(axis=0)

        # Calculate class label as a vector of proportions of each class
        class_vector = df['Category'].iloc[selected_rows]
        weight_df = pd.DataFrame({'Category':list(class_vector),'weight':list(weights)})

        # Pivot the DataFrame
        pivot_df = weight_df.pivot_table(index=weight_df.index, columns='Category', values='weight', aggfunc='sum')

        # Fill NaN values with 0
        pivot_df = pivot_df.fillna(0)

        # Ensure all possible classes exist in the DataFrame
        for class_ in all_class:
            if class_ not in pivot_df.columns:
                pivot_df[class_] = 0.0

        #sort and sum
        pivot_sum = pivot_df.sort_index(axis=1).sum(axis=0)

        # Append class_vector to new row
        new_row = pd.concat([new_row,pivot_sum],axis=0)

        # Append new row to synthetic dataframe
        df_synthetic.append(pd.DataFrame(new_row))
        if (i%1000)==0:
            print(f'done row {i}, {((i/nsamp)*100)}% done')
    df_synthetic = pd.concat(df_synthetic,axis=1)
    df_synthetic = df_synthetic.transpose()
    return df_synthetic