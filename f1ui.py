import streamlit as st
from Functions1 import *
import matplotlib.pyplot as plt
import time

st.set_page_config(
    page_title="F1 Analytics",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center;'>
        F1 Analytics Dashboard
    </h1>

    <h4 style='text-align:center; color:grey;'>
        Explore Formula 1 Data
    </h4>
    """,
    unsafe_allow_html=True
)

st.sidebar.header(
    "Race Settings"
)

year = st.sidebar.number_input(
    "Year",
    min_value=2018,
    max_value=2026,
    value=2025,
    key="year_input"
)

gp = st.sidebar.text_input(
    "Grand Prix",
    "Monaco",
    key="gp_input"
)

session_type = st.sidebar.selectbox(
    "Session Type",
    [
        "Race",
        "Qualifying",
        "Practice"
    ],
    key="session_input"
)

driver = (
    st.sidebar.text_input(
        "Driver Code",
        "HAM",
        key="driver_input"
    )
    .upper()
)

driver_list = (
    st.sidebar.text_input(
        "Compare Drivers",
        "HAM,VER,LEC",
        key="driver_compare"
    )
    .upper()
)

load_button = st.sidebar.button(
    "Load Session"
)

session_map = {
    "Race": "R",
    "Qualifying": "Q"
}


def get_fastest_lap(
    session,
    driver_code
):

    try:

        lap = (
            session.laps
            .pick_drivers(
                driver_code
            )
            .pick_fastest()
        )

        return lap

    except:
        return None


def add_turns(
    ax,
    session
):

    try:

        circuit_info = (
            session
            .get_circuit_info()
        )

        for _, corner in (
            circuit_info
            .corners
            .iterrows()
        ):

            ax.axvline(
                x=corner[
                    "Distance"
                ],
                linestyle="--",
                alpha=0.3
            )

            ax.text(
                corner[
                    "Distance"
                ],
                ax.get_ylim()[1]
                * 0.98,
                f"T{corner['Number']}",
                fontsize=8,
                rotation=90,
                verticalalignment="top"
            )

    except:
        pass


def speed_trace_plot(
    session,
    driver_code,
    title
):

    fastest_lap = (
        get_fastest_lap(
            session,
            driver_code
        )
    )

    if fastest_lap is None:

        st.error(
            f"Invalid Driver: "
            f"{driver_code}"
        )

        return

    telemetry = (
        fastest_lap
        .get_car_data()
        .add_distance()
    )

    fig, ax = plt.subplots(
        figsize=(12, 6)
    )

    ax.plot(
        telemetry[
            "Distance"
        ],
        telemetry[
            "Speed"
        ]
    )

    add_turns(
        ax,
        session
    )

    ax.set_title(
        title
    )

    ax.set_xlabel(
        "Distance (m)"
    )

    ax.set_ylabel(
        "Speed (km/h)"
    )

    ax.grid()

    st.pyplot(fig)


def draw_track_map(
    session,
    driver
):

    try:

        fastest_lap = (
            get_fastest_lap(
                session,
                driver
            )
        )

        if fastest_lap is None:
            return

        pos = (
            fastest_lap
            .get_pos_data()
        )

        fig, ax = plt.subplots(
            figsize=(8, 8)
        )

        ax.plot(
            pos["X"],
            pos["Y"],
            linewidth=3
        )

        ax.axis(
            "equal"
        )

        ax.grid()

        circuit_info = (
            session
            .get_circuit_info()
        )

        for _, corner in (
            circuit_info
            .corners
            .iterrows()
        ):

            ax.scatter(
                corner["X"],
                corner["Y"]
            )

            ax.text(
                corner["X"],
                corner["Y"],
                f"T{corner['Number']}",
                fontsize=9
            )

        st.pyplot(fig)

    except:
        st.warning(
            "Track map unavailable"
        )


if load_button:

    try:

        if (
            session_type
            == "Practice"
        ):

            sessions = {}

            for fp in [
                "FP1",
                "FP2",
                "FP3"
            ]:

                try:

                    sessions[
                        fp
                    ] = (
                        load_session(
                            year,
                            gp,
                            fp
                        )
                    )

                except:
                    pass

            st.session_state[
                "practice_sessions"
            ] = sessions

        else:

            session = (
                load_session(
                    year,
                    gp,
                    session_map[
                        session_type
                    ]
                )
            )

            st.session_state[
                "session"
            ] = session

        st.session_state[
            "loaded"
        ] = True

        st.session_state[
            "year"
        ] = year

        st.session_state[
            "gp"
        ] = gp

        st.session_state[
            "session_type"
        ] = session_type

    except Exception as e:

        st.error(
            f"Error: {e}"
        )


if (
    "loaded"
    in st.session_state
):

    year = (
        st.session_state[
            "year"
        ]
    )

    gp = (
        st.session_state[
            "gp"
        ]
    )

    session_type = (
        st.session_state[
            "session_type"
        ]
    )

    st.success(
        "Session Loaded"
    )

    st.subheader(
        f"{year} "
        f"{gp} "
        f"- "
        f"{session_type}"
    )

    if (
        session_type
        == "Practice"
    ):

        sessions = (
            st.session_state[
                "practice_sessions"
            ]
        )

        fig, ax = plt.subplots(
            figsize=(12, 6)
        )

        colors = {
            "FP1": "blue",
            "FP2": "orange",
            "FP3": "green"
        }

        for fp in sessions:

            lap = (
                get_fastest_lap(
                    sessions[fp],
                    driver
                )
            )

            if lap is None:
                continue

            telemetry = (
                lap
                .get_car_data()
                .add_distance()
            )

            ax.plot(
                telemetry[
                    "Distance"
                ],
                telemetry[
                    "Speed"
                ],
                label=fp,
                color=colors[
                    fp
                ]
            )

        add_turns(
            ax,
            list(
                sessions
                .values()
            )[0]
        )

        ax.legend()
        ax.grid()

        st.pyplot(fig)

    else:

        session = (
            st.session_state[
                "session"
            ]
        )

        option = st.selectbox(
            "Choose Data",
            [
                "Race Results",
                "Lap Times",
                "Driver Comparison",
                "Speed Trace",
                "Tyre Strategy"
            ]
            if session_type
            == "Race"
            else [
                "Single Driver Speed Trace",
                "Driver Comparison"
            ]
        )

        if (
            option
            == "Race Results"
        ):

            st.dataframe(
                get_results(
                    session
                )
            )

        elif (
            option
            == "Lap Times"
        ):

            laps = (
                session.laps
                .pick_drivers(
                    driver
                )
            )

            lap_times = (
                laps[
                    "LapTime"
                ]
                .dt
                .total_seconds()
            )

            fig, ax = plt.subplots()

            ax.plot(
                laps[
                    "LapNumber"
                ],
                lap_times
            )

            ax.grid()

            st.pyplot(fig)

        elif (
            option
            in [
                "Speed Trace",
                "Single Driver Speed Trace"
            ]
        ):

            speed_trace_plot(
                session,
                driver,
                f"{driver} Speed Trace"
            )

        elif (
            option
            == "Driver Comparison"
        ):

            compare_list = [
                d.strip()
                for d in (
                    driver_list
                    .split(",")
                )
            ]

            fig, ax = plt.subplots(
                figsize=(12, 6)
            )

            for d in (
                compare_list
            ):

                lap = (
                    get_fastest_lap(
                        session,
                        d
                    )
                )

                if lap is None:
                    continue

                telemetry = (
                    lap
                    .get_car_data()
                    .add_distance()
                )

                ax.plot(
                    telemetry[
                        "Distance"
                    ],
                    telemetry[
                        "Speed"
                    ],
                    label=d
                )

            add_turns(
                ax,
                session
            )

            ax.legend()
            ax.grid()

            st.pyplot(fig)

        elif (
            option
            == "Tyre Strategy"
        ):

            laps = (
                session.laps
                .pick_drivers(
                    driver
                )
            )

            tyre_strategy = []

            current = None
            start = None

            for _, lap in (
                laps.iterrows()
            ):

                tyre = lap[
                    "Compound"
                ]

                lap_num = lap[
                    "LapNumber"
                ]

                if tyre != current:

                    if (
                        current
                        is not None
                    ):

                        tyre_strategy.append(
                            (
                                current,
                                start,
                                prev_lap
                            )
                        )

                    current = tyre
                    start = lap_num

                prev_lap = lap_num

            tyre_strategy.append(
                (
                    current,
                    start,
                    prev_lap
                )
            )

            for (
                tyre,
                start,
                end
            ) in tyre_strategy:

                st.write(
                    f"{tyre}: "
                    f"{int(start)}"
                    f" - "
                    f"{int(end)}"
                )

    st.subheader(
        "Track Map"
    )

    if (
        session_type
        == "Practice"
    ):

        draw_track_map(
            list(
                st.session_state[
                    "practice_sessions"
                ]
                .values()
            )[-1],
            driver
        )

    else:

        draw_track_map(
            session,
            driver
        )
