[![CircleCI](https://circleci.com/gh/yizhang7210/Acre.svg?style=svg)](https://circleci.com/gh/yizhang7210/Acre)

# Acre
Algorithmically Constructed Rates Explorer

## Overview
Acre is a set of web APIs that predicts short term profitable price changes in
the [retail margin foreign exchange market](https://en.wikipedia.org/wiki/Retail_foreign_exchange_trading).

In particular, at the end of every trading day (5pm America/New York time), Acre
publishes the predicted profitable price change through the next trading day for
a number of currency pairs according to multiple algorithms.

For example, at 17:00 New York time on May 15 2018, one of Acre's algorithms may
predict the profitable price change for the currency pair EUR/USD to be 25 pips
(percentage in points). This means that according to this algorithm, the bid price
of EUR/USD at 17:00 on May 16 will be 0.0025 higher than the ask price of EUR/USD
at 17:00 on May 15.

On the other hand, if the prediction is -34 pips on USD/JPY, this means that the
algorithm thinks the ask price at the end of the day will be 0.34 lower than the
bid price at the start of the day.

## Usage
To use Acre's prediction service, please refer to Acre's API documentation [here](http://api-dev.acre.one/v1/docs)

## Contribute
To contribute to Acre, please refer to the developer documentation [here](docs/dev/Getting-Started.md).
