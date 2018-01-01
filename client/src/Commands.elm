module Commands exposing (..)

import Http
import Json.Decode as Decode
import Json.Decode.Pipeline exposing (decode, required)
import Msgs exposing (Msg)
import Models exposing (Named, Prediction)
import RemoteData


baseUrl : String
baseUrl =
    "http://api-dev.acre.one/v1/"


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


fetchPredictions : String -> Int -> Cmd Msg
fetchPredictions algo limit =
    let
        url =
            baseUrl
                ++ "algos/"
                ++ algo
                ++ "/predicted_changes?order_by=-date&limit="
                ++ (toString limit)
    in
        Http.get url (Decode.list predictionDecoder)
            |> RemoteData.sendRequest
            |> Cmd.map Msgs.OnFetchPredictions


nameDecoder : Decode.Decoder (Named {})
nameDecoder =
    Decode.map (\name -> { name = name })
        (Decode.at [ "name" ] Decode.string)


predictionDecoder : Decode.Decoder Prediction
predictionDecoder =
    Decode.map5 Prediction
        (Decode.at [ "date" ] Decode.string)
        (Decode.at [ "instrument" ] Decode.string)
        (Decode.at [ "predictor" ] Decode.string)
        (Decode.at [ "predicted_change" ] Decode.float)
        (Decode.at [ "score" ] Decode.float)
