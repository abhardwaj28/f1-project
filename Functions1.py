```python id="krx3n2"
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

    try:

        session = (
            fastf1.get_session(
                year,
                gp,
                session_type
            )
        )

        session.load(
            telemetry=True,
            weather=False,
            messages=False
        )

        return session

    except Exception as e:

        raise Exception(
            f"Session failed "
            f"to load: {e}"
        )


def get_results(
    session
):

    try:

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

    except:

        return None
```
