import pandas as pd
import numpy as np
from datetime import datetime
import random

np.random.seed(42)
random.seed(42)

models = {
    'Veda Spark':   {'segment': 'Hatchback',    'fuel': 'Petrol',  'base_price': 600000,  'cost': 480000},
    'Veda Cruise':  {'segment': 'Sedan',         'fuel': 'Petrol',  'base_price': 1050000, 'cost': 800000},
    'Veda Storm P': {'segment': 'Compact SUV',   'fuel': 'Petrol',  'base_price': 1400000, 'cost': 1020000},
    'Veda Storm C': {'segment': 'Compact SUV',   'fuel': 'CNG',     'base_price': 1550000, 'cost': 1100000},
    'Veda Terra':   {'segment': 'Full SUV',      'fuel': 'Diesel',  'base_price': 1950000, 'cost': 1450000},
    'Veda Volt':    {'segment': 'Electric SUV',  'fuel': 'EV',      'base_price': 2250000, 'cost': 1750000},
}

regions = ['North', 'South', 'West', 'East']

dealers = {
    'North': ['Delhi Central', 'Noida Prime', 'Gurgaon Auto', 'Lucknow Motors', 'Chandigarh Veda'],
    'South': ['Bangalore Elite', 'Chennai Drive', 'Hyderabad Motors', 'Kochi Veda', 'Coimbatore Auto'],
    'West':  ['Mumbai Premium', 'Pune Central', 'Ahmedabad Veda', 'Surat Motors', 'Nashik Auto'],
    'East':  ['Kolkata Drive', 'Bhubaneswar Veda', 'Patna Motors', 'Ranchi Auto', 'Guwahati Veda'],
}

monthly_volumes = {
    'Veda Spark':   [980, 950, 920, 880, 840, 790, 740, 700, 660, 620, 580, 540],
    'Veda Cruise':  [420, 430, 415, 440, 425, 410, 400, 390, 385, 375, 360, 350],
    'Veda Storm P': [680, 710, 740, 760, 790, 810, 780, 740, 700, 670, 640, 610],
    'Veda Storm C': [210, 220, 230, 245, 260, 275, 290, 305, 315, 320, 325, 330],
    'Veda Terra':   [380, 395, 410, 430, 450, 470, 490, 510, 525, 540, 555, 570],
    'Veda Volt':    [120, 135, 150, 170, 195, 220, 250, 280, 310, 340, 370, 400],
}

region_weights = {
    'Veda Spark':   {'North': 0.38, 'South': 0.25, 'West': 0.27, 'East': 0.10},
    'Veda Cruise':  {'North': 0.30, 'South': 0.28, 'West': 0.28, 'East': 0.14},
    'Veda Storm P': {'North': 0.32, 'South': 0.26, 'West': 0.30, 'East': 0.12},
    'Veda Storm C': {'North': 0.28, 'South': 0.30, 'West': 0.30, 'East': 0.12},
    'Veda Terra':   {'North': 0.28, 'South': 0.30, 'West': 0.32, 'East': 0.10},
    'Veda Volt':    {'North': 0.12, 'South': 0.42, 'West': 0.35, 'East': 0.11},
}

discount_rates = {
    'Veda Spark':   [0.030,0.032,0.031,0.033,0.034,0.036,0.038,0.040,0.042,0.044,0.046,0.048],
    'Veda Cruise':  [0.025,0.025,0.026,0.026,0.027,0.027,0.028,0.030,0.031,0.032,0.033,0.034],
    'Veda Storm P': [0.020,0.020,0.021,0.021,0.022,0.022,0.035,0.045,0.050,0.052,0.053,0.054],
    'Veda Storm C': [0.018,0.018,0.019,0.019,0.019,0.020,0.020,0.020,0.021,0.021,0.022,0.022],
    'Veda Terra':   [0.015,0.015,0.015,0.016,0.016,0.016,0.017,0.017,0.017,0.018,0.018,0.018],
    'Veda Volt':    [0.010,0.010,0.010,0.010,0.011,0.011,0.011,0.012,0.012,0.012,0.013,0.013],
}

# All 12 months
months = [
    (1,'Jan'),(2,'Feb'),(3,'Mar'),(4,'Apr'),(5,'May'),(6,'Jun'),
    (7,'Jul'),(8,'Aug'),(9,'Sep'),(10,'Oct'),(11,'Nov'),(12,'Dec')
]

records = []
counter = 1

for month_idx, (month_num, month_name) in enumerate(months):
    for model_name, model_info in models.items():
        total_units = monthly_volumes[model_name][month_idx]
        rw = region_weights[model_name]

        # Storm P price hike from August (month_idx >= 7)
        price_multiplier = 1.08 if (model_name == 'Veda Storm P' and month_idx >= 7) else 1.0
        base_price = model_info['base_price'] * price_multiplier
        cost = model_info['cost']
        discount_rate = discount_rates[model_name][month_idx]

        for region in regions:
            region_units = max(1, int(total_units * rw[region] + np.random.randint(-5, 6)))
            dealer_list = dealers[region]

            for _ in range(region_units):
                dealer = random.choice(dealer_list)
                unit_price = base_price * (1 + np.random.uniform(-0.02, 0.02))
                discount_amt = unit_price * discount_rate
                selling_price = unit_price - discount_amt
                gross_profit = selling_price - cost
                sale_day = random.randint(1, 28)

                # Format date as DD-MON-YY for Oracle
                sale_date = f"{sale_day:02d}-{month_name.upper()}-24"

                records.append({
                    'TRANSACTION_ID':   f'VA2024{month_num:02d}{counter:05d}',
                    'SALE_DATE':        sale_date,
                    'YEAR':             2024,
                    'MONTH':            month_num,
                    'MONTH_NAME':       month_name,
                    'MODEL':            model_name,
                    'SEGMENT':          model_info['segment'],
                    'FUEL_TYPE':        model_info['fuel'],
                    'REGION':           region,
                    'DEALER':           dealer,
                    'BASE_PRICE':       round(base_price, 0),
                    'DISCOUNT_AMOUNT':  round(discount_amt, 0),
                    'SELLING_PRICE':    round(selling_price, 0),
                    'COST_PRICE':       cost,
                    'GROSS_PROFIT':     round(gross_profit, 0),
                    'GROSS_MARGIN_PCT': round((gross_profit / selling_price) * 100, 2),
                    'UNITS_SOLD':       1,
                })
                counter += 1

df = pd.DataFrame(records)
df.to_csv('/home/claude/VedaAuto_Sales_Data_V2.csv', index=False)

print("=" * 50)
print("  VEDAAUTO V2 — DATA GENERATION COMPLETE")
print("=" * 50)
print(f"  Total Rows     : {len(df):,}")
print(f"  Months         : {df['MONTH'].nunique()} (all 12)")
print(f"  Models         : {df['MODEL'].nunique()}")
print(f"  Regions        : {df['REGION'].nunique()}")
print("=" * 50)
print("\nMonthly check:")
print(df.groupby(['MONTH','MONTH_NAME'])['UNITS_SOLD'].sum().to_string())
