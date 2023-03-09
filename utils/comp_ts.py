import streamlit as st

from utils.aux_dicts import (
    dict_actor_inter,
    dict_options_ts_cats,
    dict_options_ts_viz,
    dict_options_ts_agg_period,
    options_agg,
    options_viz_timeframe,
)
from utils.duckdb_queries import load_actor_cats_data, load_actor_cats_data_n_months

from utils.viz_plotly import (
    create_ts_plotly_viz
)

from utils.acled_actor_transform import (
    rehydrate_actor_df,
    create_time_series_df
)

from utils.df_to_dict import (
    df_cols_to_dict_admin1,
    df_cols_to_dict_event,
    df_cols_to_dict_sub_event,
    df_cols_to_dict_admin0,
    df_cols_to_dict_actor
)

path_to_actor_db = "data/acled_actor_db.parquet"
path_to_actor_dict = "data/acled_actor_dict.parquet"
path_to_event_dict = "data/acled_event_dict.parquet"
path_to_sub_event_dict = "data/acled_sub_event_dict.parquet"
path_to_admin0_dict = "data/admin0_dict.parquet"
path_to_admin1_dict = "data/admin1_dict.csv"

# Loading the dictionaries
dict_admin0 = df_cols_to_dict_admin0(path_to_admin0_dict, "GID_0", "COUNTRY")
dict_admin1 = df_cols_to_dict_admin1(path_to_admin1_dict, "ADMIN1_ID", "ADMIN1_NAME")
dict_actor = df_cols_to_dict_actor(path_to_actor_dict, "ACTOR_ID", "ACTOR_NAME")
dict_event = df_cols_to_dict_event(path_to_event_dict, "EVENT_TYPE_ID", "EVENT_TYPE")
dict_sub_event = df_cols_to_dict_sub_event(path_to_sub_event_dict, "SUB_EVENT_TYPE_ID", "SUB_EVENT_TYPE")


def create_comp_ts(actor, months):
    st.subheader("Zeitreihen")
    with st.expander("Einstellungen"):
        col_ts_1, col_ts_2, col_ts_3, col_ts_4, col_ts_5 = st.columns(5)
        with col_ts_1:
            sel_ts_mode = st.radio(
                "**Aggregationsart**",
                options=tuple(options_agg.keys()),
                format_func=lambda x: options_agg[x],
                key="mode_ts"
            )
        with col_ts_2:
            sel_ts_timeframe = st.radio(
                "**Betrachtungszeitraum**",
                options=tuple(options_viz_timeframe.keys()),
                format_func=lambda x: options_viz_timeframe[x],
                key="timeframe_ts"
            )
        with col_ts_3:
            sel_ts_cats = st.radio(
                "**Kategorien**",
                options=tuple(dict_options_ts_cats.keys()),
                format_func=lambda x: dict_options_ts_cats[x],
                key="cats_ts"
            )
        with col_ts_4:
            sel_ts_viz = st.radio(
                "**Diagrammoptionen**",
                options=tuple(dict_options_ts_viz.keys()),
                format_func=lambda x: dict_options_ts_viz[x],
                key="viz_ts"
            )
        with col_ts_5:
            sel_ts_agg_period = st.selectbox(
                "**Aggregationsperioden**",
                options = list(dict_options_ts_agg_period.keys()),
                format_func=lambda x: dict_options_ts_agg_period[x],
                index=3,
                key="agg_ts"
            )
    if sel_ts_timeframe == "all_times":
        df = load_actor_cats_data(actor)
    elif sel_ts_timeframe == "last_n_months":
        df = load_actor_cats_data_n_months(actor, months)

    df_decoded = rehydrate_actor_df(df,
                                     dict_actor,
                                     dict_event,
                                     dict_sub_event,
                                     dict_admin0,
                                     dict_admin1,
                                     dict_actor_inter)

    df_ts = create_time_series_df(df_decoded, sel_ts_cats, sel_ts_agg_period, sel_ts_timeframe, months)
    st.plotly_chart(
        create_ts_plotly_viz(df_ts, sel_ts_mode, sel_ts_cats, sel_ts_agg_period, sel_ts_viz),
        use_container_width=True)

