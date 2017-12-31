module Commands exposing (..)

import Http
import Json.Decode as Decode
import Json.Decode.Pipeline exposing (decode, required)
import Msgs exposing (Msg)
import Models exposing (Instrument, Algo)
import RemoteData


baseUrl : String
baseUrl =
    "http://api-dev.acre.one/v1/"


fetchInstruments : Cmd Msg
fetchInstruments =
    Http.get (baseUrl ++ "instruments") instrumentsDecoder
        |> RemoteData.sendRequest
        |> Cmd.map Msgs.OnFetchInstruments


instrumentsDecoder : Decode.Decoder (List Instrument)
instrumentsDecoder =
    Decode.list instrumentDecoder


instrumentDecoder : Decode.Decoder Instrument
instrumentDecoder =
    decode Instrument
        |> required "name" Decode.string
        |> required "multiplier" Decode.int


fetchAlgos : Cmd Msg
fetchAlgos =
    Http.get (baseUrl ++ "algos") algosDecoder
        |> RemoteData.sendRequest
        |> Cmd.map Msgs.OnFetchAlgos


algosDecoder : Decode.Decoder (List Algo)
algosDecoder =
    Decode.list algoDecoder


algoDecoder : Decode.Decoder Algo
algoDecoder =
    decode Algo
        |> required "name" Decode.string
        |> required "description" Decode.string
