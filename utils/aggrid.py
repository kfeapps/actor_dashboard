from st_aggrid import AgGrid, GridOptionsBuilder


def create_aggrid(df_temp,
                  cols_to_hide = ["DATA_ID", "TIME_PRECISION", "LATITUDE", "LONGITUDE", "GEO_PRECISION", "TIMESTAMP",
                                  "ACTOR_TYPE", "ACTORS_ASSOC", "ACTORS_OPP_ASSOC", "INTER_ACTOR", "INTER_ACTOR_OPP",
                                  "__index_level_0__", "INTERACTION"]):
    gb = GridOptionsBuilder.from_dataframe(df_temp)
    gb.configure_default_column(filterable=True, groupable=True)
    gb.configure_column("EVENT_DATE", header_name="Datum Ereignis", initialSort="desc", maxWidth=150)
    gb.configure_column("EVENT_TYPE", header_name="Hauptereignistyp", maxWidth=150)
    gb.configure_column("SUB_EVENT_TYPE", header_name="Nebenereignistyp")
    gb.configure_column("FATALITIES", header_name="Konflikttote", maxWidth=150)
    gb.configure_column("GID_0", header_name="Land", maxWidth=150)
    gb.configure_column("GID_1", header_name="ADMIN1-Region")
    gb.configure_column("ACTOR", header_name="Akteur")
    gb.configure_column("ACTOR_OPP", header_name="gegnerischer Akteur", minWidth=300)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5)
    for col in cols_to_hide:
        gb.configure_column(col, hide=True)
    gridOptions = gb.build()
    AgGrid(df_temp,
           gridOptions=gridOptions)
