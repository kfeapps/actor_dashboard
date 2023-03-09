import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def create_plotly_sunburst_chart(df_, title, cat_cols=["EVENT_TYPE", "SUB_EVENT_TYPE"], agg_type='sum'):
    if agg_type == 'sum':
        df_ = df_[df_["FATALITIES"] != 0]
    grouped_df = df_.groupby(cat_cols).agg({'FATALITIES': agg_type}).reset_index()
    fig = px.sunburst(grouped_df,
                      path=cat_cols,
                      values='FATALITIES',
                      branchvalues='total',
                      maxdepth=2,
                      title=title)
    fig.update_layout(uniformtext=dict(minsize=12, mode='hide'))
    return fig


def create_plotly_treemap_chart(df_, title, cat_cols=["EVENT_TYPE", "SUB_EVENT_TYPE"], agg_type='sum'):
    if agg_type == 'sum':
        df_ = df_[df_["FATALITIES"] != 0]
        grouped_df = df_.groupby(cat_cols).agg({'FATALITIES': agg_type}).reset_index()
    elif agg_type == "count":
        grouped_df = df_.groupby(cat_cols).agg({'FATALITIES': agg_type}).reset_index()
    fig = px.treemap(grouped_df,
                     path=[px.Constant("Alle")] + cat_cols,
                     values='FATALITIES',
                     maxdepth=3,
                     width=700,
                     height=700,
                     title=title)
    fig.update_layout(uniformtext=dict(minsize=10, mode='hide'))
    return fig


def create_plotly_icicle_chart(df_, title, cat_cols=["EVENT_TYPE", "SUB_EVENT_TYPE"], agg_type='sum'):
    if agg_type == 'sum':
        df_ = df_[df_["FATALITIES"] != 0]
    grouped_df = df_.groupby(cat_cols).agg({'FATALITIES': agg_type}).reset_index()
    fig = px.icicle(grouped_df,
                    path=[px.Constant("Alle")] + cat_cols,
                    values='FATALITIES',
                    title=title
                    )
    fig.update_layout(uniformtext=dict(minsize=10, mode='hide'))
    return fig


def create_dist_plotly_viz(df_, dist_mode, dist_cats, dist_viz):
    if dist_mode == 'EVENTS':
        agg_type = 'count'
        mode_description = "Ereignisse"
    elif dist_mode == 'FATALITIES':
        agg_type = 'sum'
        mode_description = "Konflikttote"
    if dist_cats == "admin0_admin1":
        list_cats = ["GID_0", "GID_1"]
        cats_description = " (Land, ADMIN1-Region)"
    elif dist_cats == "inter_opp_actor_opp":
        list_cats = ["INTER_ACTOR_OPP", "ACTOR_OPP"]
        cats_description = " gegnerischer (Akteurstyp, Akteur)"
    elif dist_cats == "event_types_sub_event_types":
        list_cats = ["EVENT_TYPE", "SUB_EVENT_TYPE"]
        cats_description = " (Hauptereignistyp, Nebenereignistyp)"
    if dist_viz == "sunburst":
        title = "Sunburst-Diagramm: Übersicht " + mode_description + cats_description
        fig = create_plotly_sunburst_chart(df_,title, list_cats, agg_type)
    elif dist_viz == "treemap":
        title = "Treemap-Diagramm: Übersicht " + mode_description + cats_description
        fig = create_plotly_treemap_chart(df_,title, list_cats, agg_type)
    elif dist_viz == "icicle":
        title = "Icicle-Diagramm: Übersicht " + mode_description + cats_description
        fig = create_plotly_icicle_chart(df_, title, list_cats, agg_type)
    return fig


def create_ts_plotly_viz(df_, mode, cats, agg_period, viz):
    df = df_.set_index("EVENT_DATE").sort_index()
    ts_df = df.pivot_table(index=df.index, columns=cats, values=mode, aggfunc='sum')
    ts_df = ts_df.fillna(0)

    if viz == "area":
        traces = []
        for column in ts_df.columns:
            trace = go.Scatter(
                x=ts_df.index,
                y=ts_df[column],
                mode='lines',
                stackgroup='one',
                name=column
            )
            traces.append(trace)

        # Define the layout for the chart
        layout = go.Layout(
            title='Flächendiagramm',
            hovermode='x',
            yaxis=dict(range=[0, None])
        )

        # Create the figure and display the chart
        fig = go.Figure(data=traces, layout=layout)
        fig.update_layout(barmode='stack')

    if viz == "line":
        traces = []
        for column in ts_df.columns:
            trace = go.Scatter(
                x=ts_df.index,
                y=ts_df[column],
                mode='lines+markers',
                name=column
            )
            traces.append(trace)

        layout = go.Layout(
            hovermode='x',
            title='Multi-Liniendiagramm',
            yaxis=dict(range=[0,None])
        )
        fig = go.Figure(data=traces, layout=layout)
    return fig


