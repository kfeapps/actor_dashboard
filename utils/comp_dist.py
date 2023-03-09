from utils.acled_actor_transform import rehydrate_actor_df
from utils.aux_dicts import options_agg, options_viz_timeframe, options_dist_cats, options_dist_viz, dict_actor_inter
import streamlit as st

from utils.duckdb_queries import load_actor_cats_data, load_actor_cats_data_n_months
from utils.viz_plotly import create_dist_plotly_viz

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


def create_comp_dist(actor, months):
    st.subheader("Verteilungen")
    with st.expander("Einstellungen"):
        col_dist_1, col_dist_2, col_dist_3, col_dist_4 = st.columns(4)
        with col_dist_1:
            sel_dist_mode = st.radio(
                "**Aggregationsart**",
                options=tuple(options_agg.keys()),
                format_func=lambda x: options_agg[x]
            )
        with col_dist_2:
            sel_dist_timeframe = st.radio(
                "**Betrachtungszeitraum**",
                options=tuple(options_viz_timeframe.keys()),
                format_func=lambda x: options_viz_timeframe[x],
            )
        with col_dist_3:
            sel_dist_cats = st.radio(
                "**Kategorien**",
                options=tuple(options_dist_cats.keys()),
                format_func=lambda x: options_dist_cats[x],
            )
        with col_dist_4:
            sel_dist_viz = st.radio(
                "**Diagrammoptionen**",
                options=tuple(options_dist_viz.keys()),
                format_func=lambda x: options_dist_viz[x],
                index=1
            )

    if sel_dist_timeframe == "all_times":
        df_cats = load_actor_cats_data(actor)
    elif sel_dist_timeframe == "last_n_months":
        df_cats = load_actor_cats_data_n_months(actor, months)

    df_cats_decoded = rehydrate_actor_df(df_cats,
                                         dict_actor,
                                         dict_event,
                                         dict_sub_event,
                                         dict_admin0,
                                         dict_admin1,
                                         dict_actor_inter)

    st.plotly_chart(
        create_dist_plotly_viz(df_cats_decoded, sel_dist_mode, sel_dist_cats, sel_dist_viz),
        use_container_width=True)
