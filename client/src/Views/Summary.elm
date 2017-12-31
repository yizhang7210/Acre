module Views.Summary exposing (..)

import Html exposing (Html, div, text, ul, li)
import Msgs exposing (Msg)
import Models exposing (Model, Instrument, Algo)
import RemoteData exposing (WebData)


view : Model -> Html Msg
view model =
    div []
        [ maybeList model.instruments
        , maybeList2 model.algos
        ]


list : List Instrument -> Html Msg
list ins =
    ins
        |> List.map (\l -> li [] [ text l.name ])
        |> ul []


maybeList : WebData (List Instrument) -> Html Msg
maybeList response =
    case response of
        RemoteData.NotAsked ->
            text ""

        RemoteData.Loading ->
            text "Loading..."

        RemoteData.Success ins ->
            list ins

        RemoteData.Failure error ->
            text (toString error)


list2 : List Algo -> Html Msg
list2 ins =
    ins
        |> List.map (\l -> li [] [ text l.name ])
        |> ul []


maybeList2 : WebData (List Algo) -> Html Msg
maybeList2 response =
    case response of
        RemoteData.NotAsked ->
            text ""

        RemoteData.Loading ->
            text "Loading..."

        RemoteData.Success algo ->
            list2 algo

        RemoteData.Failure error ->
            text (toString error)
