import pandas as pd
import streamlit as st
import datetime
import duckdb
from st_aggrid import AgGrid, GridOptionsBuilder
import plotly.express as px
import utils.comp_ts
import utils.comp_dist
import utils.comp_table
import utils.comp_new_info
import utils.comp_overview
import utils.comp_maps

from streamlit_option_menu import option_menu

from utils.aux_dicts import (
    dict_actor_types,
    dict_actor_inter,
    dict_options_ts_cats,
    dict_options_ts_viz,
    dict_options_ts_agg_period,
    options_dist_cats,
    options_agg,
    options_viz_timeframe,
    options_dist_viz
)

from utils.viz_plotly import (
    create_dist_plotly_viz,
    create_ts_plotly_viz
)
from utils.aggrid import create_aggrid
from utils.duckdb_queries import (
    load_actor_data,
    get_actor_list_with_filters,
    get_first_event_date,
    get_last_event_date,
    get_last_fat_date,
    get_first_fat_date,
    get_total_fat,
    get_total_events,
    get_fat_last_n_months,
    get_events_last_n_months,
    get_new_regions,
    get_new_opposing_actors,
    load_actor_cats_data,
    load_actor_cats_data_n_months
)
from utils.df_to_dict import (
    df_cols_to_dict_admin1,
    df_cols_to_dict_event,
    df_cols_to_dict_sub_event,
    df_cols_to_dict_admin0, df_cols_to_dict_actor
)
from utils.acled_actor_transform import (
    rehydrate_actor_df,
    create_regions_table,
    create_actor_opp_table,
    rehydrate_actor_event_cats_df,
    create_time_series_df
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

with st.sidebar:
    st.subheader("Filtereinstellungen")
    sel_actor_types = st.radio(
        "Verwendete Akteurstypen",
        options=("incl_main_actors", "incl_assoc_actors"),
        index=0,
        format_func=lambda x: dict_actor_types[x]
    )
    sel_countries = st.multiselect(
        "Länderauswahl",
        options=list(dict_admin0.keys()),
        default=["AFG"],
        format_func=lambda x: dict_admin0[x]
    )
    sel_timeframe = st.date_input(
        "Zeitraum auswählen",
        value=[datetime.date(1997, 1, 1), datetime.date.today()],
        min_value=datetime.date(1997, 1, 1),
        max_value=datetime.date.today()
    )
    st.subheader("Feineinstellungen")
    sel_months_back = st.number_input(
        "Vergleichszeitraum in Monaten",
        value=12,
        min_value=1
    )

sel_menu = option_menu(None,
                       ["Neue Infos", "Tabelle", "Verteilungen", "Zeitreihe", "Karten"],
                       icons=['clipboard-data', 'table', 'pie-chart', 'graph-up', 'map'],
                       menu_icon="cast",
                       default_index=4,
                       orientation="horizontal")

st.header("Faktenübersicht Akteure")


if sel_countries and len(sel_timeframe) == 2:
    sel_actor = st.selectbox(
        "Akteursauswahl",
        options=get_actor_list_with_filters(sel_actor_types, sel_countries, sel_timeframe),
        index=0,
        format_func=lambda x: dict_actor[x]
    )
    df_sel_actor = load_actor_data(sel_actor)
    df_sel_actor_decoded = rehydrate_actor_df(df_sel_actor, dict_actor, dict_event, dict_sub_event, dict_admin0, dict_admin1, dict_actor_inter)

    utils.comp_overview.create_comp_overview(sel_actor, sel_months_back)

    if sel_menu == "Neue Infos":
        utils.comp_new_info.create_comp_new_info(sel_actor, sel_months_back)
    if sel_menu == "Tabelle":
        utils.comp_table.create_comp_tables(df_sel_actor_decoded)
    if sel_menu == "Verteilungen":
        utils.comp_dist.create_comp_dist(sel_actor, sel_months_back)
    if sel_menu == "Zeitreihe":
        utils.comp_ts.create_comp_ts(sel_actor, sel_months_back)
    if sel_menu == "Karten":
        utils.comp_maps.create_comp_maps(sel_actor, sel_months_back)


