# SalesProcessing
Lynray Barends

1) Reads in Sales and Region files.
2) Enriches the Sales records with region descriptions
3) Outputs the summarised TotalSalesAmount and NumberOfSales per Region and Network to the 'Data/Output' Folder
4) Archives the processed sales to 'Data/Archive'

## Prerequisites:
 - Python 3.5
 - pandas
 - datetime
 - glob
 - os

## File Structure

Data
|
-- Region
|
-- Sales
|
-- Output
|
-- Archive

## Run
- python process_sales.py

## Assumptions made:
- The most current region description is the one that will be used.
  - This was assumed, because I noticed that the previous region description for Region 3 was 'Eastern Western Region', which did not make sense.
- If there is no current region description - then the region description at that time is null (if we had to enrich the data at a point where the most current region description had been ended, but no new one was added)
- There is a maximum of one current region description at a time, per Region
- Person cannot buy the same product in same region + network on the same day  - if this was the case, there would be duplicates rows in the Sales table.

## Scale Notes and Limitation
- I have used Pandas for the solution. This may become inefficient as dataset scales up beyond 10 million Records
