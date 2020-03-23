# Stock Market Data Analyzer

This tool will help on analyzing stock prices data.

## Getting Started

This instruction will help you understand the way to use this tool. 

### Description

It's a tool to analyzing stock prices if you put the stock codes and term in "Setting.ini" under the folder named "conf".

```
Setting.ini

[DEFAULT]
period = weekly

code = 9434, 9020, 9434

```

### Installing

No need to install the tool.

## Running

3 steps to running the tool:
    1. Add and save both target stock codes and term in the Setting.ini.
    2. Run the main.py.
    3. Check the result in a folder named with the data

```
20200319.log

2020-03-23 10:44:04,774: INFO:        Found 3 valid codes.
2020-03-23 10:44:04,780: INFO:        STOCK CODE: 9020, 9143, 9434
2020-03-23 10:44:04,785: INFO:        
2020-03-23 10:44:10,120: INFO:        Found URLs related to 9020 (East Japan Railway Company).
2020-03-23 10:44:10,124: INFO:        10 URLs found.
2020-03-23 10:44:10,125: INFO:        
2020-03-23 10:44:12,197: INFO:        Found URLs related to 9143 (SG HOLDINGS CO.,LTD.).
2020-03-23 10:44:12,197: INFO:        4 URLs found.
2020-03-23 10:44:12,201: INFO:        
2020-03-23 10:44:13,472: INFO:        Found URLs related to 9434 (SoftBank Corp.).
2020-03-23 10:44:13,476: INFO:        3 URLs found.
2020-03-23 10:44:13,479: INFO:        
2020-03-23 10:44:16,563: INFO:        Accumulated data with URLs related to 9020.
2020-03-23 10:44:16,563: INFO:        
2020-03-23 10:44:17,799: INFO:        Accumulated data with URLs related to 9143.
2020-03-23 10:44:17,803: INFO:        
2020-03-23 10:44:18,669: INFO:        Accumulated data with URLs related to 9434.
2020-03-23 10:44:18,673: INFO:        
2020-03-23 10:44:18,786: INFO:        Exporting average data...(9020)
2020-03-23 10:44:18,790: INFO:        
2020-03-23 10:44:18,790: INFO:        Exporting average data...(9143)
2020-03-23 10:44:18,806: INFO:        
2020-03-23 10:44:18,809: INFO:        Exporting average data...(9434)
2020-03-23 10:44:18,822: INFO:        
2020-03-23 10:44:18,884: INFO:        TIME : 15.87612009048462 (s)


```

### Sequence diagram

![Sequence diagram](https://github.com/ChiamingMike/stock_collector/blob/image/stock_collector/Sequence%20diagram.png)

### Release version

ver 0.0.0 : 
1. Collecting data to calculate the average values.
2. Exporting data as CSV file.

