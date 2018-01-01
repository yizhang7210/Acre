module Views.Summary exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Msgs exposing (Msg)
import Models as M
import Dict exposing (Dict)


view : M.Model -> Html Msg
view model =
    div []
        [ table [ style [ ( "text-align", "center" ) ] ]
            [ thead [] [ generateHeader model.instruments ]
            , tbody [] [ generateRows model ]
            ]
        ]


generateHeader : List String -> Html Msg
generateHeader instruments =
    instruments
        |> List.map (\ins -> th [] [ text ins ])
        |> (::) (th [] [])
        |> tr []


generateRows : M.Model -> Html Msg
generateRows model =
    getPredictions model
        |> (::) (td [] [ text "Euler" ])
        |> tr []


getPredictions : M.Model -> List (Html Msg)
getPredictions model =
    model.instruments
        |> List.map (getPredictionFromInstrument model)
        |> List.map (\x -> td [] [ text x ])


getPredictionFromInstrument : M.Model -> String -> String
getPredictionFromInstrument model ins =
    model.predictions
        |> Dict.get ins
        |> Maybe.withDefault M.emptyPrediction
        |> .predicted_change
        |> toString
