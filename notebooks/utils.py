import os, glob, pickle
import pandas as pd
import numpy as np


def chunk_loader(directory, c_size=100_000, orient='columns', lines=True, read_limit=0, index_col=0, low_memory=False):
    """
    Reads a directory in chunks, infers type if json or csv format
    directory(str) = location of file
    c_size(int) = size of individual chunk
    oritnet(str) = orientation of expected format
    read_limit(int) = limit of file to read
    index_col(int) = Column(s) to use as the row labels
    """
    
    if '.json' in directory:
        #return JsonReader object
        review_df_chunk = pd.read_json(directory, orient=orient,lines=lines, chunksize=c_size)
    elif '.csv' in directory:
        if 'zip' in directory:
            compression='zip'
        else:
            compression = 'infer'
        review_df_chunk = pd.read_csv(directory,
                                      chunksize=c_size,
                                      index_col=index_col,
                                      low_memory= low_memory,
                                      compression=compression)
    else:
        print('unsopported file type, must be json or csv')
        return None
        
    #keep track of file limit
    limit=0
    
    #store chunks in list
    chunk_list = []
    
    #loop over chunks
    for df in review_df_chunk:
        #add to limit
        limit += df.shape[0]
        #append to list
        chunk_list.append(df)
        
        #check if a limit was set
        if read_limit>0:
            if limit >=read_limit:
                df= pd.concat(chunk_list)
                return df.loc[:read_limit-1,:]
        
    #combine results in one dataframe
    df= pd.concat(chunk_list)
    
    
    return df


