import streamlit as st

from utils.acled_actor_transform import create_regions_table, create_actor_opp_table
from utils.df_to_dict import df_cols_to_dict_admin0, df_cols_to_dict_admin1, df_cols_to_dict_actor, \
    df_cols_to_dict_event, df_cols_to_dict_sub_event
from utils.duckdb_queries import get_new_regions, get_new_opposing_actors


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


def create_comp_new_info(actor, months):
    with st.expander(f"Neue aktive Regionen in den letzten {months} Monaten"):
        st.markdown(create_regions_table(get_new_regions(actor, months), dict_admin1, dict_admin0))
    with st.expander(f"Neue gegnerische Akteure in neuen Regionen in den letzten {months} Monate"):
        st.markdown(create_actor_opp_table(get_new_opposing_actors(actor, months) ,dict_admin1, dict_admin0, dict_actor))
