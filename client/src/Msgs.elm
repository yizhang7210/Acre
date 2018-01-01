module Msgs exposing (..)

import Models exposing (Prediction, Named)
import RemoteData exposing (WebData)


type Msg
    = OnFetchInstruments (WebData (List (Named {})))
    | OnFetchAlgos (WebData (List (Named {})))
    | OnFetchPredictions (WebData (List Prediction))
