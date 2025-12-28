# Forecast Data Pipeline  
**API → Python → SQLite → Pandas**

## Overview
This project implements a lightweight end-to-end data pipeline that retrieves weather forecast data from a public API, processes it using Python, stores it in a SQLite database, and performs analytical operations with Pandas.

The repository demonstrates core backend data engineering concepts with a clear and reproducible workflow.

## Data Source
Forecast data is collected from the **Open-Meteo public API**.  
The pipeline retrieves hourly forecasts for the next three days, including:
- Temperature (°C)
- Relative humidity (%)
- Wind speed (km/h)

Cities included:
- London  
- New York  
- Tokyo  
- Sydney  
- Reykjavik  

## Pipeline Flow
1. Fetch forecast data via HTTP requests  
2. Parse and normalize nested JSON responses  
3. Convert data into a structured tabular format  
4. Store cleaned data in a SQLite database  
5. Load data into Pandas DataFrames  
6. Perform aggregations and analytical calculations  

## Database Design
- **Database**: SQLite  
- **Table**: `forecasts`  

Each row represents an hourly forecast containing:
- City  
- Forecast timestamp  
- Temperature  
- Humidity  
- Wind speed  

The table is recreated on each run to ensure clean results.

## Analysis Performed
The project computes:
- Maximum predicted temperature per city  
- City with the highest predicted temperature overall  
- Average wind speed per city  
- City with the highest average wind speed  
- Temperature swing (max–min) over the forecast period  
- Average temperature per city  
- Count of high-humidity conditions (≥ 90%)  

## Technologies Used
- Python  
- Requests  
- SQLite  
- Pandas  
- NumPy  

## Scope
This project focuses on backend data processing and analysis only.  
No frontend, visualization, or API service layer is included.

## Purpose
Designed as an exam-ready and portfolio-friendly example demonstrating API ingestion, relational storage, and Pandas-based data analysis.
