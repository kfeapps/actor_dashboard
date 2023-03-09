import pandas as pd
import streamlit as st
from pandas.tseries.offsets import MonthEnd, QuarterEnd, YearEnd

def rehydrate_actor_df(df_, actor_dict, event_dict, sub_event_dict, admin0_dict, admin1_dict, inter_actor_dict):
    df_["ACTOR"] = df_["ACTOR"].map(actor_dict)
    df_["ACTOR_OPP"] = df_["ACTOR_OPP"].map(actor_dict)
    df_["EVENT_TYPE"] = df_["EVENT_TYPE"].map(event_dict)
    df_["GID_0"] = df_["GID_0"].map(admin0_dict)
    df_["GID_1"] = df_["GID_1"].map(admin1_dict)
    df_["SUB_EVENT_TYPE"] = df_["SUB_EVENT_TYPE"].map(sub_event_dict)
    df_["INTER_ACTOR_OPP"] = df_["INTER_ACTOR_OPP"].map(inter_actor_dict)
    return df_


def rehydrate_actor_event_cats_df(df_, event_dict, sub_event_dict):
    df_["SUB_EVENT_TYPE"] = df_["SUB_EVENT_TYPE"].map(sub_event_dict)
    df_["EVENT_TYPE"] = df_["EVENT_TYPE"].map(event_dict)
    return df_


@st.cache_data
def create_regions_table(df_, admin1_dict, admin0_dict):
    df_["GID_1"] = df_["GID_1"].map(admin1_dict)
    df_["GID_0"] = df_["GID_0"].map(admin0_dict)
    df_ = df_.sort_values(["FIRST_OCCURENCE"], ascending=False)
    df_["FIRST_OCCURENCE"] = df_["FIRST_OCCURENCE"].apply(lambda x: x.strftime('%Y-%m-%d'))
    df_ = df_.rename(columns={"GID_1": "ADMIN1-Regionen", "GID_0": "Land", "FIRST_OCCURENCE": "Erste Aktivität"})
    return df_.to_markdown(index=False)


@st.cache_data
def create_actor_opp_table(df_, admin1_dict, admin0_dict, actor_dict):
    df_ = df_[df_["ACTOR_OPP"]!=0]
    df_["GID_1"] = df_["GID_1"].map(admin1_dict)
    df_["GID_0"] = df_["GID_0"].map(admin0_dict)
    df_["ACTOR_OPP"] = df_["ACTOR_OPP"].map(actor_dict)
    df_ = df_.sort_values(["FIRST_OCCURENCE"], ascending=False)
    df_["FIRST_OCCURENCE"] = df_["FIRST_OCCURENCE"].apply(lambda x: x.strftime('%Y-%m-%d'))
    df_ = df_.rename(columns={"GID_1": "ADMIN1-Regionen",
                              "GID_0": "Land",
                              "FIRST_OCCURENCE": "Erste Aktivität",
                              "ACTOR_OPP": "gegnerischer Akteur"})
    return df_.to_markdown(index=False)


def create_time_series_df(df_,agg_cateories, agg_period, ts_timeframe, months):
    if ts_timeframe == "last_n_months":
        date_limit = pd.Timestamp.today().normalize() - pd.DateOffset(months=months)
        df_filtered = df_[df_["EVENT_DATE"] >= date_limit]
    else:
        df_filtered = df_.copy()

    df_grouped = df_filtered.groupby(
        [
            pd.Grouper(key="EVENT_DATE", freq=agg_period),
            pd.Grouper(key=agg_cateories)

        ]
    ).agg(
        FATALITIES = pd.NamedAgg(column="FATALITIES", aggfunc="sum"),
        EVENTS = pd.NamedAgg(column="FATALITIES", aggfunc="count")
    )
    return df_grouped.reset_index()


def create_maps_df(df_, ts_timeframe, months):
    if ts_timeframe == "last_n_months":
        date_limit = pd.Timestamp.today().normalize() - pd.DateOffset(months=months)
        df_filtered = df_[df_["EVENT_DATE"] >= date_limit]
    else:
        df_filtered = df_.copy()
    df_filtered["END_MONTH"] = (df_filtered["EVENT_DATE"] + MonthEnd(0)).dt.strftime('%Y-%m-%d')
    df_filtered["END_QUARTER"] = (df_filtered["EVENT_DATE"] + QuarterEnd()).dt.strftime('%Y-%m-%d')
    df_filtered["END_YEAR"] = (df_filtered["EVENT_DATE"] + YearEnd()).dt.strftime('%Y-%m-%d')
    return df_filtered