module Commands exposing (..)

import Http
import Json.Decode as Decode
import Json.Decode.Pipeline exposing (decode, required)
import Msgs exposing (Msg)
import Models exposing (Named, Prediction)
import RemoteData
import Dict exposing (Dict)


baseUrl : String
baseUrl =
    "http://api-dev.acre.one/v1/"


fetchCurrentDate : Cmd Msg
fetchCurrentDate =
    Http.get (baseUrl ++ "trading_day/current") dateDecoder
        |> RemoteData.sendRequest
        |> Cmd.map Msgs.OnFetchCurrentTradingDay


fetchInstruments : Cmd Msg
fetchInstruments =
    Http.get (baseUrl ++ "instruments") (Decode.list nameDecoder)
        |> RemoteData.sendRequest
        |> Cmd.map Msgs.OnFetchInstruments


fetchAlgos : Cmd Msg
fetchAlgos =
    Http.get (baseUrl ++ "algos") (Decode.list nameDecoder)
        |> RemoteData.sendRequest
        |> Cmd.map Msgs.OnFetchAlgos


fetchPredictions : String -> String -> Cmd Msg
fetchPredictions algo currentDate =
    let
        url =
            baseUrl
                ++ "algos/"
                ++ algo
                ++ "/predicted_changes?order_by=instrument&start="
                ++ currentDate
                ++ "&end="
                ++ currentDate
    in
        Http.get url (Decode.list predictionDecoder)
            |> RemoteData.sendRequest
            |> Cmd.map Msgs.OnFetchPredictions


nameDecoder : Decode.Decoder (Named {})
nameDecoder =
    Decode.map (\name -> { name = name })
        (Decode.at [ "name" ] Decode.string)


dateDecoder : Decode.Decoder (Dict String String)
dateDecoder =
    Decode.map (\date -> Dict.singleton "date" date)
        (Decode.at [ "date" ] Decode.string)


predictionDecoder : Decode.Decoder Prediction
predictionDecoder =
    Decode.map5 Prediction
        (Decode.at [ "date" ] Decode.string)
        (Decode.at [ "instrument" ] Decode.string)
        (Decode.at [ "predictor" ] Decode.string)
        (Decode.at [ "predicted_change" ] Decode.float)
        (Decode.at [ "score" ] Decode.float)
