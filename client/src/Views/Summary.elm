module Views.Summary exposing (..)

import Html exposing (..)
import Html.Attributes exposing (..)
import Msgs exposing (Msg)
import Models exposing (Model, Instrument, Algo)


view : Model -> Html Msg
view model =
    div []
        [ table [ style [ ( "text-align", "center" ) ] ]
            [ thead [] [ generateHeader model.instruments ]
            , tbody [] [ generateRows model ]
            ]
        ]


generateRows : Model -> Html Msg
generateRows model =
    tr []
        [ td [] [ text "Euler" ]
        , td [] [ text "0.1" ]
        , td [] [ text "0.2" ]
        , td [] [ text "0.3" ]
        , td [] [ text "0.4" ]
        , td [] [ text "0.5" ]
        ]


generateHeader : List String -> Html Msg
generateHeader instruments =
    instruments
        |> List.map (\ins -> th [] [ text ins ])
        |> (::) (th [] [])
        |> tr []
