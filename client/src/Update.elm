module Update exposing (..)

import Dict exposing (Dict)
import Msgs exposing (Msg(..))
import Models exposing (Model, Named, Prediction)
import Commands exposing (fetchAlgos)
import RemoteData


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Msgs.OnFetchCurrentTradingDay response ->
            ( { model | currentTradingDay = getField "date" response }
            , Commands.fetchInstruments
            )

        Msgs.OnFetchInstruments response ->
            ( { model | instruments = getNames response |> List.sort }
            , Commands.fetchAlgos
            )

        Msgs.OnFetchAlgos response ->
            ( { model | algos = getNames (response) }
            , Commands.fetchPredictions "euler" model.currentTradingDay
            )

        Msgs.OnFetchPredictions response ->
            ( { model | predictions = getContent (response) }
            , Cmd.none
            )


getField : String -> RemoteData.WebData (Dict String String) -> String
getField key response =
    case response of
        RemoteData.NotAsked ->
            ""

        RemoteData.Loading ->
            ""

        RemoteData.Success content ->
            Dict.get key content |> Maybe.withDefault ""

        RemoteData.Failure error ->
            toString error


getNames : RemoteData.WebData (List (Named a)) -> List String
getNames response =
    case response of
        RemoteData.NotAsked ->
            []

        RemoteData.Loading ->
            []

        RemoteData.Success content ->
            List.map (.name) content

        RemoteData.Failure error ->
            [ toString error ]


getContent : RemoteData.WebData (List Prediction) -> Dict String Prediction
getContent response =
    case response of
        RemoteData.NotAsked ->
            Dict.empty

        RemoteData.Loading ->
            Dict.empty

        RemoteData.Success content ->
            List.foldl (\p ps -> Dict.insert p.instrument p ps) Dict.empty content

        RemoteData.Failure error ->
            Dict.empty
