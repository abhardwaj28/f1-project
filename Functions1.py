import fastf1
import streamlit as st
import os

cache_dir = "cache"

if not os.path.exists(
    cache_dir
):
    os.makedirs(
        cache_dir
    )

fastf1.Cache.enable_cache(
    cache_dir
)


@st.cache_resource
def load_session(
    year,
    gp,
    session_type
):

    session = (
        fastf1.get_session(
            year,
            gp,
            session_type
        )
    )

    session.load()

    return session


def get_results(
    session
):

    return session.results[
        [
            "Position",
            "Abbreviation",
            "FullName",
            "TeamName",
            "Points"
        ]
    ]

