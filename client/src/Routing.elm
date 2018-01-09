module Routing exposing (..)

import Navigation exposing (Location)
import Models exposing (Route(..))
import UrlParser exposing (..)


matchers : Parser (Route -> a) a
matchers =
    oneOf
        [ map SummaryRoute top
        , map AlgoHistoryRoute (s "algos" </> string)
        ]


parseLocation : Location -> Route
parseLocation location =
    case (parseHash matchers location) of
        Just route ->
            route

        Nothing ->
            NotFoundRoute


algoHistoryPath : String -> String
algoHistoryPath algo =
    "#algos/" ++ algo
