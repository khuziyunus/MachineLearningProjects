import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# 1. Generate all business days (Mon–Fri) from Jan 1, 2021 to Jun 21, 2025
date_range = pd.date_range(start="2021-01-01", end="2025-06-21", freq='B')  # 'B' means business day

# 2. Function to scrape PPL OHLC data for a specific date
def fetch_ppl_ohlc(date_str):
    url = 'https://dps.psx.com.pk/historical'
    headers = {"User-Agent": "Mozilla/5.0"}
    payload = {'date': date_str}

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find_all('tr', {'data-type': 'equity'})

        for row in rows:
            cols = row.find_all('td')
            if cols and cols[0].text.strip() == "PPL":
                return {
                    'date': date_str,
                    'open': cols[1].text.strip(),
                    'high': cols[2].text.strip(),
                    'low': cols[3].text.strip(),
                    'close': cols[4].text.strip()
                }
    except Exception as e:
        print(f"Error on {date_str}: {e}")
    
    return None

# 3. Loop over dates and gather data
data = []
for i, date in enumerate(date_range):
    date_str = date.strftime('%Y-%m-%d')
    print(f"[{i+1}/{len(date_range)}] Fetching: {date_str}")
    row = fetch_ppl_ohlc(date_str)
    if row:
        data.append(row)

# 4. Convert to DataFrame and save
df = pd.DataFrame(data)
print(df.head())
df.to_csv("PPL_Daily_OHLC_2021_2025.csv", index=False)
