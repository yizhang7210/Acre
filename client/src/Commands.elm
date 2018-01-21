module Commands exposing (..)

import Http
import Json.Decode as Decode
import Msgs exposing (Msg)
import Models as M
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


fetchPredictions : M.AlgoName -> String -> String -> String -> Cmd (RemoteData.WebData (List M.DailyChange))
fetchPredictions algo startDate endDate orderBy =
    let
        url =
            baseUrl
                ++ "algos/"
                ++ String.toLower algo
                ++ "/predicted_changes?order_by="
                ++ orderBy
                ++ "&start="
                ++ startDate
                ++ "&end="
                ++ endDate
    in
        Http.get url (Decode.list predictedChangeDecoder)
            |> RemoteData.sendRequest


fetchPredictionSummary : M.Model -> Cmd Msg
fetchPredictionSummary model =
    fetchPredictions "Euler" model.currentTradingDay model.currentTradingDay "instrument"
        |> Cmd.map Msgs.OnFetchPredictionSummary


fetchPastPredictedChanges : M.AlgoName -> String -> Cmd Msg
fetchPastPredictedChanges algo currentDate =
    let
        startDate =
            addYear -1 currentDate
    in
        fetchPredictions algo startDate currentDate "instrument,-date"
            |> Cmd.map (Msgs.OnFetchHistoricalPredictedChanges algo)


fetchPastProfitableChanges : M.AlgoName -> String -> Cmd Msg
fetchPastProfitableChanges algo currentDate =
    let
        startDate =
            addYear -1 currentDate

        url =
            baseUrl
                ++ "algos/"
                ++ String.toLower algo
                ++ "/profitable_changes?order_by=instrument,date&start="
                ++ startDate
                ++ "&end="
                ++ currentDate
    in
        Http.get url (Decode.list profitableChangeDecoder)
            |> RemoteData.sendRequest
            |> Cmd.map (Msgs.OnFetchHistoricalProfitableChanges algo)


nameDecoder : Decode.Decoder (M.Named {})
nameDecoder =
    Decode.map (\name -> { name = name })
        (Decode.at [ "name" ] Decode.string)


dateDecoder : Decode.Decoder (Dict String String)
dateDecoder =
    Decode.map (\date -> Dict.singleton "date" date)
        (Decode.at [ "date" ] Decode.string)


predictedChangeDecoder : Decode.Decoder M.DailyChange
predictedChangeDecoder =
    Decode.map3 M.DailyChange
        (Decode.at [ "date" ] Decode.string)
        (Decode.at [ "instrument" ] Decode.string)
        (Decode.at [ "predicted_change" ] Decode.float)


profitableChangeDecoder : Decode.Decoder M.DailyChange
profitableChangeDecoder =
    Decode.map3 M.DailyChange
        (Decode.at [ "date" ] Decode.string)
        (Decode.at [ "instrument" ] Decode.string)
        (Decode.at [ "profitable_change" ] Decode.float)


addYear : Int -> String -> String
addYear diffYear currentDate =
    String.left 4 currentDate
        |> String.toInt
        |> Result.withDefault 0
        |> (+) diffYear
        |> toString
        |> (flip (++)) (String.right 6 currentDate)
