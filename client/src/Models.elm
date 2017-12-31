module Models exposing (..)

import RemoteData exposing (WebData)


type alias Model =
    { instruments : WebData (List Instrument)
    , algos : WebData (List Algo)
    }


type alias Algo =
    { name : String, description : String }


type alias Instrument =
    { name : String, multipler : Int }


initialModel : Model
initialModel =
    { instruments = RemoteData.Loading
    , algos = RemoteData.Loading
    }
