SELECT COUNT(*) FROM vedaauto_sales;

Monthly Performance Overview
SELECT 
    month,
    month_name,
    SUM(units_sold)                     AS total_units,
    ROUND(SUM(selling_price)/100000, 2) AS revenue_lakhs,
    ROUND(SUM(gross_profit)/100000, 2)  AS profit_lakhs,
    ROUND(AVG(gross_margin_pct), 2)     AS avg_margin_pct
FROM vedaauto_sales
GROUP BY month, month_name
ORDER BY month;

Model wise Sales & Profitability Analysis
SELECT 
    model,
    segment,
    fuel_type,
    SUM(units_sold)                     AS total_units,
    ROUND(SUM(selling_price)/100000, 2) AS revenue_lakhs,
    ROUND(SUM(gross_profit)/100000, 2)  AS profit_lakhs,
    ROUND(AVG(gross_margin_pct), 2)     AS avg_margin_pct
FROM vedaauto_sales
GROUP BY model, segment, fuel_type
ORDER BY total_units DESC

Veda Volt Monthly Growth Trend
SELECT 
    month,
    month_name,
    model,
    SUM(units_sold) AS total_units
FROM vedaauto_sales
WHERE model = 'Veda Volt'
GROUP BY month, month_name, model
ORDER BY month;

Region wise Performance Analysis
SELECT 
    region,
    SUM(units_sold)                     AS total_units,
    ROUND(SUM(selling_price)/100000, 2) AS revenue_lakhs,
    ROUND(SUM(gross_profit)/100000, 2)  AS profit_lakhs,
    ROUND(AVG(gross_margin_pct), 2)     AS avg_margin_pct
FROM vedaauto_sales
GROUP BY region
ORDER BY total_units DESC;

Veda Volt Regional Distribution
SELECT 
    region,
    model,
    SUM(units_sold) AS total_units
FROM vedaauto_sales
WHERE model = 'Veda Volt'
GROUP BY region, model
ORDER BY total_units DESC;

Discount & Margin Trend Analysis
SELECT 
    model,
    month,
    month_name,
    ROUND(AVG(discount_amount),0)  AS avg_discount,
    ROUND(AVG(gross_margin_pct),2) AS avg_margin_pct
FROM vedaauto_sales
WHERE model IN ('Veda Storm P','Veda Spark')
GROUP BY model, month, month_name
ORDER BY model, month

Top 10 Dealer Performance
SELECT * FROM (
    SELECT 
        dealer,
        region,
        SUM(units_sold)                     AS total_units,
        ROUND(SUM(selling_price)/100000, 2) AS revenue_lakhs,
        ROUND(AVG(gross_margin_pct), 2)     AS avg_margin_pct
    FROM vedaauto_sales
    GROUP BY dealer, region
    ORDER BY total_units DESC
)
WHERE ROWNUM <= 10;

Segment wise Profitability Analysis
SELECT 
    segment,
    SUM(units_sold)                     AS total_units,
    ROUND(SUM(selling_price)/100000, 2) AS revenue_lakhs,
    ROUND(SUM(gross_profit)/100000, 2)  AS profit_lakhs,
    ROUND(AVG(gross_margin_pct), 2)     AS avg_margin_pct
FROM vedaauto_sales
GROUP BY segment
ORDER BY total_units DESC;

What-If Price Scenario Analysis
SELECT 
    model,
    SUM(units_sold)                        AS current_units,
    ROUND(SUM(selling_price)/100000, 2)    AS current_revenue,
    ROUND(SUM(selling_price)*1.05/100000, 2) AS revenue_if_5pct_price_up,
    ROUND(SUM(selling_price)*0.95/100000, 2) AS revenue_if_5pct_price_down
FROM vedaauto_sales
WHERE model IN ('Veda Volt','Veda Storm P')
GROUP BY model;

Final Model Profitability Summary
SELECT 
    model,
    segment,
    SUM(units_sold)                     AS total_units,
    ROUND(SUM(selling_price)/100000, 2) AS revenue_lakhs,
    ROUND(SUM(gross_profit)/100000, 2)  AS profit_lakhs,
    ROUND(AVG(gross_margin_pct), 2)     AS avg_margin_pct,
    ROUND(AVG(discount_amount), 0)      AS avg_discount
FROM vedaauto_sales
GROUP BY model, segment
ORDER BY profit_lakhs DESC;