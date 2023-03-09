import streamlit as st
import pandas as pd

@st.cache_data
def df_cols_to_dict_admin0(path_temp, key_col, value_col):
    df_temp = pd.read_parquet(path_temp)
    return df_temp.set_index(key_col).to_dict()[value_col]


@st.cache_data
def df_cols_to_dict_actor(path_temp, key_col, value_col):
    df_temp = pd.read_parquet(path_temp)
    return df_temp.set_index(key_col).to_dict()[value_col]


@st.cache_data
def df_cols_to_dict_event(path_temp, key_col, value_col):
    df_temp = pd.read_parquet(path_temp)
    return df_temp.set_index(key_col).to_dict()[value_col]

@st.cache_data
def df_cols_to_dict_sub_event(path_temp, key_col, value_col):
    df_temp = pd.read_parquet(path_temp)
    return df_temp.set_index(key_col).to_dict()[value_col]

@st.cache_data
def df_cols_to_dict_sub_event(path_temp, key_col, value_col):
    df_temp = pd.read_parquet(path_temp)
    return df_temp.set_index(key_col).to_dict()[value_col]


@st.cache_data
def df_cols_to_dict_admin1(path_temp, key_col, value_col):
    df_temp = pd.read_csv(path_temp)
    return df_temp.set_index(key_col).to_dict()[value_col]

