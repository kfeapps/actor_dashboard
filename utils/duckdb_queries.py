import duckdb
import streamlit as st
import pandas as pd


def get_first_events(sel_actor):
    query = f"""SELECT * 
                FROM 'data/acled_actor_db.parquet'
                WHERE ACTOR = {sel_actor}
                AND EVENT_DATE = (SELECT MIN(EVENT_DATE) FROM 'data/acled_actor_db.parquet')
    """
    return duckdb.execute(query).df()


@st.cache_data
def get_actor_list_with_filters(actor_types, countries, timeframe):
    if actor_types == "incl_main_actors":
        actor_type_codes = (1, 2)
    elif actor_types == "incl_assoc_actors":
        actor_type_codes = (1, 2, 3, 4)

    start_date = timeframe[0].strftime('%Y-%m-%d')
    end_date = timeframe[1].strftime('%Y-%m-%d')
    if countries:
        query = f""" SELECT DISTINCT ACTOR
                     FROM 'data/acled_actor_db.parquet'
                     WHERE GID_0 IN  {tuple(countries)}
                     AND ACTOR_TYPE IN {actor_type_codes}
                     AND EVENT_DATE >= ?
                     AND EVENT_DATE <= ?"""
        return duckdb.execute(query, [start_date, end_date]).df()
    else:
        return pd.DataFrame()


@st.cache_data
def load_actor_data(sel_actor):
    query = f""" SELECT *
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
    """
    return duckdb.execute(query).df()


def get_first_event_date(sel_actor):
    query = f""" SELECT MIN(EVENT_DATE) AS MIN_DATE
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
    """
    return duckdb.execute(query).df()


def get_last_event_date(sel_actor):
    query = f""" SELECT MAX(EVENT_DATE) AS MAX_DATE
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
    """
    return duckdb.execute(query).df()


def get_first_fat_date(sel_actor):
    query = f""" SELECT MIN(EVENT_DATE) AS FIRST_FAT_DATE
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
                 AND FATALITIES > 0
    """
    return duckdb.execute(query).df()


def get_last_fat_date(sel_actor):
    query = f""" SELECT MAX(EVENT_DATE) AS LAST_FAT_DATE
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
                 AND FATALITIES > 0
    """
    return duckdb.execute(query).df()


def get_total_fat(sel_actor):
    query = f""" SELECT SUM(FATALITIES) AS TOTAL_FATALITIES
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
    """
    return duckdb.execute(query).df()


def get_total_events(sel_actor):
    query = f""" SELECT COUNT(*) AS TOTAL_EVENTS
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
    """
    return duckdb.execute(query).df()


def get_events_last_n_months(sel_actor, months):
    query = f"""SELECT COUNT(*) AS TOTAL_EVENTS_LAST_N_MONTHS
    FROM 'data/acled_actor_db.parquet'
    WHERE ACTOR = {sel_actor}
    AND EVENT_DATE >= current_date - INTERVAL {months} MONTH
    """
    return duckdb.execute(query).df()


def get_fat_last_n_months(sel_actor, months):
    query = f"""SELECT SUM(FATALITIES) AS TOTAL_FAT_LAST_N_MONTHS
    FROM 'data/acled_actor_db.parquet'
    WHERE ACTOR = {sel_actor}
    AND EVENT_DATE >= current_date - INTERVAL {months} MONTH
    """
    return duckdb.execute(query).df()


@st.cache_data
def get_new_regions(sel_actor, months):
    query = f"""SELECT DISTINCT t1.GID_1, t2.GID_0, MIN(t1.EVENT_DATE) AS FIRST_OCCURENCE
    FROM 'data/acled_actor_db.parquet' t1
    JOIN 'data/acled_actor_db.parquet' t2 ON t1.GID_0 = t2.GID_0
    WHERE t1.ACTOR = {sel_actor}
    AND t1.EVENT_DATE >= current_date - INTERVAL {months} MONTH
    AND t1.GID_1 NOT IN (
          SELECT DISTINCT GID_1
          FROM 'data/acled_actor_db.parquet'
          WHERE ACTOR = {sel_actor}
          AND EVENT_DATE < current_date - INTERVAL {months} MONTH
    )
    GROUP BY t1.GID_1, t2.GID_0
    """
    return duckdb.execute(query).df()


@st.cache_data
def get_new_opposing_actors(sel_actor, months):
    query = f"""SELECT DISTINCT t1.GID_1, t2.GID_0, t1.ACTOR_OPP, MIN(t1.EVENT_DATE) AS FIRST_OCCURENCE
    FROM 'data/acled_actor_db.parquet' t1
    JOIN 'data/acled_actor_db.parquet' t2 ON t1.GID_0 = t2.GID_0
    WHERE t1.ACTOR = {sel_actor}
    AND t1.EVENT_DATE >= current_date - INTERVAL {months} MONTH
    AND t1.ACTOR_OPP NOT IN (
          SELECT DISTINCT ACTOR_OPP
          FROM 'data/acled_actor_db.parquet'
          WHERE ACTOR = {sel_actor}
          AND EVENT_DATE < current_date - INTERVAL {months} MONTH
    )
    GROUP BY t1.GID_1, t2.GID_0, t1.ACTOR_OPP
    """
    return duckdb.execute(query).df()


def load_actor_cats_data(sel_actor):
    query = f""" SELECT EVENT_DATE, EVENT_TYPE, SUB_EVENT_TYPE,ACTOR, ACTOR_OPP, INTER_ACTOR_OPP, GID_0, GID_1, FATALITIES
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
    """
    return duckdb.execute(query).df()


def load_actor_cats_data_n_months(sel_actor, months):
    query = f""" SELECT EVENT_DATE, EVENT_TYPE, SUB_EVENT_TYPE, ACTOR,  ACTOR_OPP, INTER_ACTOR_OPP, GID_0, GID_1, FATALITIES
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
                 AND EVENT_DATE >= current_date - INTERVAL {months} MONTH
    """
    return duckdb.execute(query).df()


@st.cache_data
def load_actor_maps(sel_actor):
    query = f""" SELECT EVENT_DATE, EVENT_TYPE, SUB_EVENT_TYPE, ACTOR, ACTOR_OPP, INTER_ACTOR_OPP, LATITUDE, LONGITUDE, GID_0, GID_1, FATALITIES
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
    """
    return duckdb.execute(query).df()


@st.cache_data
def load_actor_maps_data_n_months(sel_actor, months):
    query = f""" SELECT EVENT_DATE, EVENT_TYPE, SUB_EVENT_TYPE, ACTOR, ACTOR_OPP, INTER_ACTOR_OPP, LATITUDE, LONGITUDE, GID_0, GID_1, FATALITIES
                 FROM 'data/acled_actor_db.parquet'
                 WHERE ACTOR = {sel_actor}
                 AND EVENT_DATE >= current_date - INTERVAL {months} MONTH
    """
    return duckdb.execute(query).df()