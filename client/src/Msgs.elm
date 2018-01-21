module Msgs exposing (..)

import Models exposing (AlgoName, Named, DailyChange)
import RemoteData exposing (WebData)
import Dict exposing (Dict)
import Navigation exposing (Location)


type Msg
    = OnFetchCurrentTradingDay (WebData (Dict String String))
    | OnFetchInstruments (WebData (List (Named {})))
    | OnFetchAlgos (WebData (List (Named {})))
    | OnFetchPredictionSummary (WebData (List DailyChange))
    | OnFetchHistoricalPredictedChanges AlgoName (WebData (List DailyChange))
    | OnFetchHistoricalProfitableChanges AlgoName (WebData (List DailyChange))
    | OnLocationChange Location
