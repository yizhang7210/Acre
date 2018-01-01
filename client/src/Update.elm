module Update exposing (..)

import Msgs exposing (Msg(..))
import Models exposing (Model, Instrument, Algo, Named)
import Commands exposing (fetchAlgos)
import RemoteData


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Msgs.OnFetchInstruments response ->
            ( { model | instruments = getNames (response) }, Commands.fetchAlgos )

        Msgs.OnFetchAlgos response ->
            ( { model | algos = getNames (response) }, Cmd.none )


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
