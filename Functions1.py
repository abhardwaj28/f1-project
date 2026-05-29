import fastf1
import streamlit as st

fastf1.Cache.enable_cache(
    "./cache"
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

    results = (
        session.results[
            [
                "Position",
                "Abbreviation",
                "FullName",
                "TeamName",
                "Points"
            ]
        ]
    )

    return results
