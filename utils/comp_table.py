import streamlit as st
from utils.aggrid import create_aggrid


def create_comp_tables(df_temp):
    st.subheader("Tabellenansicht")
    with st.expander("Erläuterung"):
        st.write("Es ist sowohl eine Sortierung und eine Filterung der Daten sowie eine Gruppierung nach den "
                 "Kategorien einer Spalte in dieser Tabelle möglich.")
    create_aggrid(df_temp)