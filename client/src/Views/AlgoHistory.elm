module Views.AlgoHistory exposing (..)

import Dict exposing (Dict)
import Date exposing (Date)
import Time exposing (Time)
import Svg exposing (..)
import Svg.Attributes exposing (..)
import Visualization.Axis as Axis exposing (defaultOptions)
import Visualization.Scale as Scale exposing (ContinuousScale, ContinuousTimeScale)
import Visualization.Shape as Shape
import Html as H
import Html.Attributes as HA
import Msgs exposing (Msg)
import Models as M
import List.Extra as LE


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
            |> Shape.line Shape.naturalCurve
            |> d


view : M.Model -> String -> H.Html Msg
view model algo =
    H.div [ HA.style [ ( "margin-top", "30px" ) ] ]
        (List.map (drawInstrument model) model.instruments)


drawInstrument : M.Model -> M.InstrumentName -> H.Html Msg
drawInstrument model instrument =
    let
        diffData =
            getPredictionDiff model instrument
    in
        H.div [ HA.style [ ( "display", "inline-table" ) ] ]
            [ H.h4 [ HA.style [ ( "margin", "10px auto" ) ] ] [ text instrument ]
            , svg
                [ width (toString w ++ "px"), height (toString h ++ "px") ]
                [ g [ transform ("translate(" ++ toString (padding - 1) ++ ", " ++ toString (h - padding) ++ ")") ]
                    [ xAxis diffData ]
                , g [ transform ("translate(" ++ toString (padding - 1) ++ ", " ++ toString padding ++ ")") ]
                    [ yAxis ]
                , g [ transform ("translate(" ++ toString padding ++ ", " ++ toString padding ++ ")") ]
                    [ Svg.path
                        [ line (List.map (\p -> ( Tuple.first p, 0 )) diffData)
                        , stroke "grey"
                        , strokeWidth "2px"
                        , strokeDasharray "5, 5"
                        , fill "none"
                        ]
                        []
                    ]
                , g [ transform ("translate(" ++ toString padding ++ ", " ++ toString padding ++ ")") ]
                    [ Svg.path
                        [ line diffData
                        , stroke "blue"
                        , strokeWidth "1px"
                        , fill "none"
                        ]
                        []
                    ]
                ]
            ]


getPredictionDiff : M.Model -> M.InstrumentName -> List ( Date, Float )
getPredictionDiff model instrument =
    let
        predictedList =
            Dict.get instrument model.pastPredictedChanges |> Maybe.withDefault []

        actualList =
            Dict.get instrument model.pastProfitableChanges |> Maybe.withDefault []

        calcDiff p a =
            (sign (p * a)) * (abs (p - a))

        getDiff pList aList =
            LE.zip pList aList
                |> List.map (\( p, a ) -> ( toDate p.date, calcDiff p.value a.value ))
    in
        getDiff predictedList actualList


sign : Float -> Float
sign n =
    if n > 0 then
        1
    else if n < 0 then
        -1
    else
        0


toDate : String -> Date
toDate dateString =
    Date.fromString dateString |> Result.withDefault (Date.fromTime 0)
