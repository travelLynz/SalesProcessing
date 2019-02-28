import pandas as pd
from datetime import datetime as dt
import glob
import os


def readin_dir(path,files):
    print ('Processing', path)
    print (len(files), 'file(s)')
    results = pd.concat([pd.read_csv(f) for f in files], ignore_index = True) if len(files) > 0 else None
    print ('Done')
    return results

def move_files(files, dest):
    for f in files:
        os.rename(f, os.path.join(dest, f.split('/')[-1]))
        print ("Moving", f)
    print ('All files moved')

def enrich_sales(sales, region):
    print ('Enriching Sales with RegionDescriptions')
    current_region = region[region.EndDate.isnull()]
    return pd.merge(sales, current_region[['Region', 'RegionDescription']], how='left', right_on=['Region'], left_on=['Region'])

# Readin files
sales_files = glob.glob('Data/Sales/*.csv')
sales = readin_dir('Data/Sales', sales_files)
region_files = glob.glob('Data/Region/*.csv')
region = readin_dir('Data/Region', region_files)

# Only proceeds if we have new sales and existing region data
if sales is not None and region is not None:

    # Convert column datatypes
    sales.Date = pd.to_datetime(sales.Date)
    sales['Amount'] = sales['Amount'].astype(float)
    region.StartDate = pd.to_datetime(region.StartDate)
    region.EndDate = pd.to_datetime(region.EndDate)

    # Enrich Sales with RegionDescription
    sales = enrich_sales(sales, region)

    # Get summarized totals and counts of Sales per Region and Network
    out_sales = sales.groupby(['Region','Network']) \
                        .agg({'identifier':'count','Amount':'sum'}) \
                        .rename(columns={'identifier':'NumberOfSales', 'Amount': 'TotalSalesAmount'})

    # Save the file to output Folder
    out_name = 'Data/Output/out-sales-' + str(dt.today()).split('.')[0].replace(':', '.').replace(' ', '.') + '.csv'
    print ('Saving output to', out_name)
    out_sales.to_csv(out_name)

    # Move Sales files to Archive
    move_files(sales_files, 'Data/Archive')
