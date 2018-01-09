module Models exposing (..)

import Dict exposing (Dict)


type alias Model =
    { currentTradingDay : String
    , instruments : List String
    , algos : List String
    , predictions : Dict String Prediction
    , route : Route
    }


type Route
    = SummaryRoute
    | AlgoHistoryRoute String
    | NotFoundRoute


type alias Named a =
    { a | name : String }


type alias Algo =
    { name : String, description : String }


type alias Instrument =
    { name : String, multipler : Int }


type alias Prediction =
    { date : String
    , instrument : String
    , predictor : String
    , predicted_change : Float
    , score : Float
    }


emptyPrediction : Prediction
emptyPrediction =
    { date = "1970-01-01"
    , instrument = "XXX_XXX"
    , predictor = ""
    , predicted_change = 1 / 0
    , score = 1 / 0
    }


initialModel : Route -> Model
initialModel route =
    { currentTradingDay = ""
    , instruments = []
    , algos = []
    , predictions = Dict.empty
    , route = route
    }
