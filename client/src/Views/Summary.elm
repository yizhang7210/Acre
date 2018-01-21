module Views.Summary exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Msgs exposing (Msg)
import Models as M
import Dict exposing (Dict)
import Routing exposing (algoHistoryPath)


view : M.Model -> Html Msg
view model =
    div [ style [ ( "text-align", "center" ) ] ]
        [ h4 [] [ text ("Predictions for " ++ model.currentTradingDay) ]
        , table [ style [ ( "margin-bottom", "200px" ), ( "display", "inline-table" ) ] ]
            [ thead [] [ generateHeader model.instruments ]
            , tbody [] [ generateRows model ]
            ]
        ]


generateHeader : List String -> Html Msg
generateHeader instruments =
    instruments
        |> List.map (\ins -> th [ style [ ( "font-weight", "normal" ) ] ] [ text ins ])
        |> (::) (th [] [])
        |> tr []


generateRows : M.Model -> Html Msg
generateRows model =
    getPredictions model
        |> (::) (td [] [ a [ href (algoHistoryPath "Euler") ] [ text "Euler" ] ])
        |> tr []


getPredictions : M.Model -> List (Html Msg)
getPredictions model =
    model.instruments
        |> List.map (getPredictionFromInstrument model)
        |> List.map (\x -> td [] [ text x ])


getPredictionFromInstrument : M.Model -> String -> String
getPredictionFromInstrument model ins =
    model.predictionSummary
        |> Dict.get ins
        |> Maybe.withDefault M.emptyPrediction
        |> .value
        |> toString
