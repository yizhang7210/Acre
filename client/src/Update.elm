module Update exposing (..)

import Dict exposing (Dict)
import Msgs exposing (Msg(..))
import Models exposing (..)
import Commands exposing (fetchAlgos)
import RemoteData
import Routing exposing (parseLocation)
import List.Extra exposing (groupWhile)
import List as L
import Maybe exposing (withDefault)


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
            ( { model | algos = getNames response |> List.sort }
            , Commands.fetchPredictionSummary model
            )

        Msgs.OnFetchPredictionSummary response ->
            ( { model | predictionSummary = getSummary (response) }
            , Cmd.none
            )

        Msgs.OnFetchHistoricalPredictedChanges algo response ->
            ( { model | pastPredictedChanges = groupValuesByInstrument response }
            , Commands.fetchPastProfitableChanges algo model.currentTradingDay
            )

        Msgs.OnFetchHistoricalProfitableChanges algo response ->
            ( { model | pastProfitableChanges = groupValuesByInstrument response }
            , Cmd.none
            )

        Msgs.OnLocationChange location ->
            case parseLocation location of
                Models.AlgoHistoryRoute algo ->
                    ( { model | route = Models.AlgoHistoryRoute algo }
                    , Commands.fetchPastPredictedChanges algo model.currentTradingDay
                    )

                Models.SummaryRoute ->
                    ( { model | route = Models.SummaryRoute }
                    , Cmd.none
                    )

                Models.NotFoundRoute ->
                    ( model, Cmd.none )


groupValuesByInstrument : RemoteData.WebData (List (HasInstrument a)) -> Dict InstrumentName (List (HasInstrument a))
groupValuesByInstrument response =
    case response of
        RemoteData.NotAsked ->
            Dict.empty

        RemoteData.Loading ->
            Dict.empty

        RemoteData.Success content ->
            content
                |> groupWhile (\p1 p2 -> p1.instrument == p2.instrument)
                |> L.foldl (\ps d -> Dict.insert (L.head ps |> getInstrumentName) ps d) Dict.empty

        RemoteData.Failure error ->
            Dict.empty


getInstrumentName : Maybe (HasInstrument a) -> InstrumentName
getInstrumentName aRecord =
    case aRecord of
        Nothing ->
            ""

        Just hasInstrument ->
            hasInstrument.instrument


getField : String -> RemoteData.WebData (Dict String String) -> String
getField key response =
    case response of
        RemoteData.NotAsked ->
            ""

        RemoteData.Loading ->
            ""

        RemoteData.Success content ->
            Dict.get key content |> withDefault ""

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


getSummary : RemoteData.WebData (List DailyChange) -> Dict InstrumentName DailyChange
getSummary response =
    groupValuesByInstrument response
        |> Dict.map (\ins ps -> List.head ps |> withDefault emptyPrediction)
