import streamlit as st

from utils.acled_actor_transform import rehydrate_actor_df
from utils.aggrid import create_aggrid
from utils.aux_dicts import dict_actor_inter
from utils.df_to_dict import df_cols_to_dict_admin0, df_cols_to_dict_admin1, df_cols_to_dict_actor, \
    df_cols_to_dict_event, df_cols_to_dict_sub_event
from utils.duckdb_queries import load_actor_data


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


def create_comp_tables(actor):
    df_sel_actor = load_actor_data(actor)
    df_sel_actor_decoded = rehydrate_actor_df(df_sel_actor, dict_actor, dict_event, dict_sub_event, dict_admin0,
                                              dict_admin1, dict_actor_inter)
    st.subheader("Tabellenansicht")
    with st.expander("Erläuterung"):
        st.write("Es ist sowohl eine Sortierung und eine Filterung der Daten sowie eine Gruppierung nach den "
                 "Kategorien einer Spalte in dieser Tabelle möglich.")
    create_aggrid(df_sel_actor_decoded)