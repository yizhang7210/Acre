module Views.AlgoHistory exposing (..)

import Html exposing (..)
import Html.Attributes exposing (class, value, href)
import Msgs exposing (Msg)
import Models as M


view : M.Model -> String -> Html Msg
view model algo =
    text algo
