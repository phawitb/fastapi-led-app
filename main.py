from fastapi import FastAPI
import pandas as pd
import numpy as np

n_perpage = 100

# df_provices from github to local .csv
provinces = ['bangkok','nonthaburi'] #--------------------
for province in provinces:
    url = f"https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/df_{province}.csv"
    df = pd.read_csv(url)
    df.to_csv(f'df_{province}.csv', index=False)

# Create FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Bangkok CSV API"}

# Endpoint to filter data by column (example: filter by 'district')
@app.get("/data/{province}/{page}")
def page_data(province,page):
    page = int(page)
    df = pd.read_csv(f'df_{province}.csv')
    df.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace inf values
    df.fillna(0, inplace=True)  # Replace NaN values
    data = df.to_dict(orient="records")
    
    page -= 1
    print(page*n_perpage,n_perpage*(page+1))
    data_list = data[page*n_perpage:n_perpage*(page+1)]
    data_dict = {i: data_list[i] for i in range(len(data_list))}
    return data_dict

# Endpoint to get the column names
@app.get("/columns")
def get_columns():
    return {"columns": list(df.columns)}
