module Msgs exposing (..)

import Models exposing (Prediction, Named)
import RemoteData exposing (WebData)
import Dict exposing (Dict)
import Navigation exposing (Location)


type Msg
    = OnFetchCurrentTradingDay (WebData (Dict String String))
    | OnFetchInstruments (WebData (List (Named {})))
    | OnFetchAlgos (WebData (List (Named {})))
    | OnFetchPredictions (WebData (List Prediction))
    | OnLocationChange Location
