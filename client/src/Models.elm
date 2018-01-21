module Models exposing (..)

import Dict exposing (Dict)


type alias Model =
    { currentTradingDay : String
    , instruments : List InstrumentName
    , algos : List AlgoName
    , predictionSummary : Dict InstrumentName DailyChange
    , pastPredictedChanges : Dict InstrumentName (List DailyChange)
    , pastProfitableChanges : Dict InstrumentName (List DailyChange)
    , route : Route
    }


type alias AlgoName =
    String


type alias InstrumentName =
    String


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


type alias HasInstrument a =
    { a | instrument : String }


type alias DailyChange =
    { date : String
    , instrument : String
    , value : Float
    }


emptyPrediction : DailyChange
emptyPrediction =
    { date = "1970-01-01"
    , instrument = "XXX_XXX"
    , value = 1 / 0
    }


initialModel : Route -> Model
initialModel route =
    { currentTradingDay = ""
    , instruments = []
    , algos = []
    , predictionSummary = Dict.empty
    , route = route
    , pastPredictedChanges = Dict.empty
    , pastProfitableChanges = Dict.empty
    }
