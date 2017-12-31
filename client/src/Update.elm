module Update exposing (..)

import Msgs exposing (Msg(..))
import Models exposing (Model)
import Commands exposing (fetchAlgos)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        Msgs.OnFetchInstruments response ->
            ( { model | instruments = response }, Commands.fetchAlgos )

        Msgs.OnFetchAlgos response ->
            ( { model | algos = response }, Cmd.none )
