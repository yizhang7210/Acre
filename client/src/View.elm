module View exposing (..)

import Html exposing (Html, div, text)
import Msgs exposing (Msg)
import Models exposing (Model)
import Views.Summary
import Views.AlgoHistory


view : Model -> Html Msg
view model =
    div []
        [ page model ]


page : Model -> Html Msg
page model =
    case model.route of
        Models.SummaryRoute ->
            Views.Summary.view model

        Models.AlgoHistoryRoute algo ->
            algoHistoryPage model algo

        Models.NotFoundRoute ->
            notFoundView


algoHistoryPage : Model -> String -> Html Msg
algoHistoryPage model algo =
    if List.member algo model.algos then
        Views.AlgoHistory.view model algo
    else
        notFoundView


notFoundView : Html msg
notFoundView =
    div []
        [ text "Not found"
        ]
