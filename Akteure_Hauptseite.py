import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

import datetime

# Internal modules
import utils.comp_ts
import utils.comp_dist
import utils.comp_table
import utils.comp_new_info
import utils.comp_overview
import utils.comp_maps

from utils.aux_dicts import dict_actor_types
from utils.duckdb_queries import get_actor_list_with_filters
from utils.df_to_dict import df_cols_to_dict_admin0, df_cols_to_dict_actor



# Paths to the data sources
path_to_actor_dict = "data/acled_actor_dict.parquet"
path_to_admin0_dict = "data/admin0_dict.parquet"


# Loading the dictionaries
dict_admin0 = df_cols_to_dict_admin0(path_to_admin0_dict, "GID_0", "COUNTRY")
dict_actor = df_cols_to_dict_actor(path_to_actor_dict, "ACTOR_ID", "ACTOR_NAME")


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
        default=["CIV"],
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

# Horizontal navigation/options bar
sel_menu = option_menu(None,
                       ["Neue Infos", "Tabelle", "Verteilungen", "Zeitreihe", "Karten"],
                       icons=['clipboard-data', 'table', 'pie-chart', 'graph-up', 'map'],
                       menu_icon="cast",
                       default_index=0,
                       orientation="horizontal")

st.header("Faktenübersicht Akteure")

# Condition to avoid trying to build content without proper input
if sel_countries and len(sel_timeframe) == 2:
    sel_actor = st.selectbox(
        "Akteursauswahl",
        options=get_actor_list_with_filters(sel_actor_types, sel_countries, sel_timeframe),
        index=1,
        format_func=lambda x: dict_actor[x]
    )

    utils.comp_overview.create_comp_overview(sel_actor, sel_months_back)

    if sel_menu == "Neue Infos":
        utils.comp_new_info.create_comp_new_info(sel_actor, sel_months_back)
    if sel_menu == "Tabelle":
        utils.comp_table.create_comp_tables(sel_actor)
    if sel_menu == "Verteilungen":
        utils.comp_dist.create_comp_dist(sel_actor, sel_months_back)
    if sel_menu == "Zeitreihe":
        utils.comp_ts.create_comp_ts(sel_actor, sel_months_back)
    if sel_menu == "Karten":
        utils.comp_maps.create_comp_maps(sel_actor, sel_months_back)


