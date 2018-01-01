module Models exposing (..)


type alias Model =
    { instruments : List String
    , algos : List String
    }


type alias Named a =
    { a | name : String }


type alias Algo =
    { name : String, description : String }


type alias Instrument =
    { name : String, multipler : Int }


initialModel : Model
initialModel =
    { instruments = []
    , algos = []
    }
