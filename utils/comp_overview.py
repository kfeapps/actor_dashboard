import streamlit as st

from utils.duckdb_queries import get_first_event_date, get_last_event_date, get_first_fat_date, get_last_fat_date, \
    get_total_fat, get_total_events, get_fat_last_n_months, get_events_last_n_months


def create_comp_overview(actor, months):
    first_event_date = get_first_event_date(actor).loc[0, 'MIN_DATE'].date()
    last_event_date = get_last_event_date(actor).loc[0, 'MAX_DATE'].date()
    first_fat_date = get_first_fat_date(actor).loc[0, 'FIRST_FAT_DATE'].date()
    last_fat_date = get_last_fat_date(actor).loc[0, 'LAST_FAT_DATE'].date()
    total_fat_all = int(get_total_fat(actor).loc[0, 'TOTAL_FATALITIES'])
    total_events_all = int(get_total_events(actor).loc[0, 'TOTAL_EVENTS'])
    total_fat_last_year = get_fat_last_n_months(actor, months).loc[0, 'TOTAL_FAT_LAST_N_MONTHS']
    total_events_last_year = get_events_last_n_months(actor, months).loc[0, 'TOTAL_EVENTS_LAST_N_MONTHS']

    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        st.markdown(f"**Erstes Ereignis**: {first_event_date}")
        st.markdown(f"**Anzahl der Konfliktereignisse (insgesamt)**: {total_events_all}")
    with col_2:
        st.markdown(f"**Erster Konflikttote**: {first_fat_date}")
        st.markdown(f"**Anzahl der Konflikttoten (insgesamt)**: {total_fat_all}")
    with col_3:
        st.markdown(f"**Letzter Konflikttote**: {last_fat_date}")
        st.markdown(f"**Anzahl der Konflikttoten (letzten {months} Monate)**: {total_fat_last_year}")
    with col_4:
        st.markdown(f"**Letztes Ereignis**: {last_event_date}")
        st.markdown(f"**Anzahl der Konfliktereignisse (letzten {months} Monate)**: {total_events_last_year}")
