import streamlit as st
import plotly.express as px

from utils.acled_actor_transform import rehydrate_actor_df, create_time_series_df, create_maps_df
from utils.aux_dicts import dict_options_ts_agg_period, dict_options_ts_cats, options_agg, dict_actor_inter, \
    options_viz_timeframe
from utils.df_to_dict import df_cols_to_dict_admin0, df_cols_to_dict_admin1, df_cols_to_dict_actor, \
    df_cols_to_dict_event, df_cols_to_dict_sub_event
from utils.duckdb_queries import load_actor_maps, load_actor_maps_data_n_months

dict_options_maps_viz = {
    "scatter": "Scatter Map"
}
dict_maps_agg_period = {
    "END_MONTH": "Monat",
    "END_QUARTER": "Quartal",
    "END_YEAR": "Jahr"
}


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


def create_comp_maps(actor, months):
    with st.expander("Einstellungen"):
        col_maps_1, col_maps_2, col_maps_3, col_maps_4, col_maps_5 = st.columns(5)
        with col_maps_1:
            sel_maps_mode = st.radio(
                "**Aggregationsart**",
                options=tuple(options_agg.keys()),
                format_func=lambda x: options_agg[x],
                key="mode_ts"
            )
        with col_maps_2:
            sel_maps_timeframe = st.radio(
                "**Betrachtungszeitraum**",
                options=tuple(options_viz_timeframe.keys()),
                format_func=lambda x: options_viz_timeframe[x],
                key="timeframe_ts"
            )
        with col_maps_3:
            sel_maps_cats = st.radio(
                "**Kategorien**",
                options=tuple(dict_options_ts_cats.keys()),
                format_func=lambda x: dict_options_ts_cats[x],
                key="cats_ts"
            )
        with col_maps_4:
            sel_maps_viz = st.radio(
                "**Diagrammoptionen**",
                options=tuple(dict_options_maps_viz.keys()),
                format_func=lambda x: dict_options_maps_viz[x],
                key="viz_ts"
            )
        with col_maps_5:
            sel_maps_agg_period = st.selectbox(
                "**Aggregationsperioden**",
                options = list(dict_maps_agg_period.keys()),
                format_func=lambda x: dict_maps_agg_period[x],
                index=0,
                key="agg_maps"
            )
    if sel_maps_timeframe == "all_times":
        df = load_actor_maps(actor)
    elif sel_maps_timeframe == "last_n_months":
        df = load_actor_maps_data_n_months(actor, months)

    df_decoded = rehydrate_actor_df(df,
                                     dict_actor,
                                     dict_event,
                                     dict_sub_event,
                                     dict_admin0,
                                     dict_admin1,
                                     dict_actor_inter)
    df_ts = create_maps_df(df_decoded, sel_maps_timeframe, months)
    fig = px.scatter_mapbox(df_ts.sort_values("EVENT_DATE"),
                            lat="LATITUDE",
                            lon="LONGITUDE",
                            color=sel_maps_cats,
                            size = "FATALITIES",
                            height=600,
                            width=1000,
                            animation_frame=sel_maps_agg_period,
                            zoom=3)
    fig.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig, use_container_width=True)

