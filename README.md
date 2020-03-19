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

2020-03-19 12:09:07,648: INFO:        Found 2 codes.
2020-03-19 12:09:07,649: INFO:        STOCK CODE: 9020, 9434
2020-03-19 12:09:07,649: INFO:        
2020-03-19 12:09:09,980: INFO:        Completed collecting URLs relating 9020 (ＪＲ東日本).
2020-03-19 12:09:09,982: INFO:        10 relevant URLs found.
2020-03-19 12:09:09,982: INFO:        
2020-03-19 12:09:10,716: INFO:        Completed collecting URLs relating 9434 (ソフトバンク).
2020-03-19 12:09:10,718: INFO:        3 relevant URLs found.
2020-03-19 12:09:10,719: INFO:        
2020-03-19 12:09:13,145: INFO:        Accumulated data with URLs related to 9020.
2020-03-19 12:09:13,147: INFO:        
2020-03-19 12:09:13,875: INFO:        Accumulated data with URLs related to 9434.
2020-03-19 12:09:13,879: INFO:        
2020-03-19 12:09:13,928: INFO:        Exporting average data...(9020)
2020-03-19 12:09:13,929: INFO:        
2020-03-19 12:09:13,946: INFO:        Exporting average data...(9434)
2020-03-19 12:09:13,954: INFO:        
2020-03-19 12:09:13,958: INFO:        TIME : 6.310539960861206 (s)

```

### Sequence diagram

[Sequence diagram](https://github.com/ChiamingMike/stock_collector/blob/image/stock_collector/Sequence%20diagram.png)

### Release version

ver 0.0.0 : 1. Collecting data to calculate the average values.
            2. Exporting data as CSV file.

### To do list

Will add the features as below:
    1. Downloading all stock codes list to prevent the codes that doesn't exist.
    2. Downloading other information. (e.g. every years ROE and ROA)
    3. Calculating US stock prices. (Only can get the JP stock prices at this moment)
