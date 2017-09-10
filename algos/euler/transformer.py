import datetime
import decimal

from datasource.models import candles, instruments

from .models import training_samples as ts

TWO_PLACES = decimal.Decimal('0.01')


class Transformer:
    def extract_features(self, day_candle):
        multiplier = day_candle.instrument.multiplier
        features = [
            day_candle.high_bid,
            day_candle.low_bid,
            day_candle.close_bid,
            day_candle.open_ask,
            day_candle.high_ask,
            day_candle.low_ask,
            day_candle.close_ask,
        ]
        features = [multiplier * (x - day_candle.open_bid) for x in features]
        features = [decimal.Decimal(x).quantize(TWO_PLACES) for x in features]

        return features

    def get_profitable_change(self, day_candle):
        multiplier = day_candle.instrument.multiplier
        change = 0
        if day_candle.close_bid > day_candle.open_ask:
            change = multiplier * (day_candle.close_bid - day_candle.open_ask)
        elif day_candle.close_ask < day_candle.open_bid:
            change = multiplier * (day_candle.close_ask - day_candle.open_bid)

        return decimal.Decimal(change).quantize(TWO_PLACES)

    def build_sample_row(self, candle_previous, candle_next):
        return ts.get_one(
            instrument=candle_next.instrument,
            date=candle_next.start_time.date() + datetime.timedelta(1),
            features=self.extract_features(candle_previous),
            target=self.get_profitable_change(candle_next)
        )

    def get_start_time(self, instrument):
        last_sample = ts.get_last(instrument)
        if last_sample is None:
            return datetime.datetime(2005, 1, 1)
        else:
            start_date = last_sample.date - datetime.timedelta(1)
            return datetime.datetime.combine(start_date, datetime.time())

    def run(self):
        all_new_samples = []
        for instrument in instruments.get_all():
            start_time = self.get_start_time(instrument)
            new_candles = candles.get_candles(
                instrument=instrument,
                start=start_time,
                sortBy='start_time'
            )
            for i in range(len(new_candles) - 1):
                all_new_samples.append(
                    self.build_sample_row(new_candles[i], new_candles[i + 1])
                )

        ts.insert_many(all_new_samples)
