module Msgs exposing (..)

import Models exposing (Instrument, Algo)
import RemoteData exposing (WebData)


type Msg
    = OnFetchInstruments (WebData (List Instrument))
    | OnFetchAlgos (WebData (List Algo))
