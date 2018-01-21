module Views.AlgoHistory exposing (..)

import Dict exposing (Dict)
import Date exposing (Date)
import Time exposing (Time)
import Svg exposing (..)
import Svg.Attributes exposing (..)
import Visualization.Axis as Axis exposing (defaultOptions)
import Visualization.List as List
import Visualization.Scale as Scale exposing (ContinuousScale, ContinuousTimeScale)
import Visualization.Shape as Shape
import Html as H
import Html.Attributes as HA
import Msgs exposing (Msg)
import Models as M


w : Float
w =
    600


h : Float
h =
    400


padding : Float
padding =
    30


xScale : ( Time, Time ) -> ContinuousTimeScale
xScale ( start, end ) =
    Scale.time ( Date.fromTime start, Date.fromTime end ) ( 0, w - 2 * padding )


yScale : ContinuousScale
yScale =
    Scale.linear ( -200, 200 ) ( h - 2 * padding, 0 )


xAxis : List ( Date, Float ) -> Svg msg
xAxis points =
    getBounds points
        |> xScale
        |> Axis.axis { defaultOptions | orientation = Axis.Bottom, tickCount = 5 }


getBounds : List ( Date, Float ) -> ( Time, Time )
getBounds points =
    let
        times =
            List.map (Tuple.first >> Date.toTime) points
    in
        ( List.minimum times |> Maybe.withDefault 0
        , List.maximum times |> Maybe.withDefault 0
        )


yAxis : Svg msg
yAxis =
    Axis.axis { defaultOptions | orientation = Axis.Left, tickCount = 5 } yScale


transformToLineData : ( Time, Time ) -> ( Date, Float ) -> Maybe ( Float, Float )
transformToLineData bounds ( x, y ) =
    Just ( Scale.convert (xScale bounds) x, Scale.convert yScale y )


line : List ( Date, Float ) -> Attribute msg
line points =
    let
        bounds =
            getBounds points
    in
        List.map (transformToLineData bounds) points
            |> Shape.line Shape.monotoneInXCurve
            |> d


view : M.Model -> String -> H.Html Msg
view model algo =
    H.div [ HA.style [ ( "margin-top", "30px" ) ] ]
        (List.map (drawInstrument model) model.instruments)


drawInstrument : M.Model -> M.InstrumentName -> H.Html Msg
drawInstrument model instrument =
    H.div [ HA.style [ ( "display", "inline-table" ) ] ]
        [ H.h4 [ HA.style [ ( "margin", "10px auto" ) ] ] [ text instrument ]
        , svg
            [ width (toString w ++ "px"), height (toString h ++ "px") ]
            [ g [ transform ("translate(" ++ toString (padding - 1) ++ ", " ++ toString (h - padding) ++ ")") ]
                [ xAxis (getData model.pastProfitableChanges instrument) ]
            , g [ transform ("translate(" ++ toString (padding - 1) ++ ", " ++ toString padding ++ ")") ]
                [ yAxis ]
            , g [ transform ("translate(" ++ toString padding ++ ", " ++ toString padding ++ ")") ]
                [ Svg.path [ line (getData model.pastPredictedChanges instrument), stroke "red", strokeWidth "1px", fill "none" ] []
                , Svg.path [ line (getData model.pastProfitableChanges instrument), stroke "blue", strokeWidth "1px", fill "none" ] []
                ]
            ]
        ]


getData : Dict M.InstrumentName (List M.DailyChange) -> M.InstrumentName -> List ( Date, Float )
getData dataDict instrument =
    dataDict
        |> Dict.get instrument
        |> Maybe.withDefault []
        |> List.map (\p -> ( toDate p.date, p.value ))


toDate : String -> Date
toDate dateString =
    Date.fromString dateString |> Result.withDefault (Date.fromTime 0)
