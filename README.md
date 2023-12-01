## quant_finance
This repository contains the code that I use to generate trading strategies.

## algo
The algo folder holds two simple trading algorithms.  buy_hold.py implements the buy and hold algorithm.

mr.py implements a simple, bollinger band based, mean reversion algorithm.

algo_base.py implements the back test tool which processes the end of day data and generates a buy, sell, or hold status.

if you are interested in creating additional trading strategies, you can pattern your work after mr.py

## util
the util folder contains utility functions that I use to process the daily equity data.

## data
the data folder provides sample data for Apple, Costco, and IBM.  technically I am paying for this data by using the brokerage that I use, so I can not provide any more than this.  the data format should be obvious, so you should be able to add your data if desired.

##main
the main folder shows how to call each of the provided trading strategies.

##charts
the charts folder contains some png charts showing the returns generated by some of my better trading strategies that were developed through this framework.  I am unable to provide the source code as I am actively trading them.
