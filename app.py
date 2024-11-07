import plotly.express as px
import palmerpenguins
import seaborn as sns
from shiny.express import input, ui
from shiny import render, reactive
from shinywidgets import render_plotly
from palmerpenguins import load_penguins

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Diamond's Penguin Figures", fillable=True)

with ui.sidebar ( position= "left", bg= "#B2D7D0", open= "open" ):
    ui.h2("Sidebar")

    ui.input_selectize(
        "selected_attribute",
        "Select an Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

    ui.input_numeric(id="plotly_bin_count", label="Bin Count (Plotly)", value=10)

    ui.input_slider(id="seaborn_bin_count", label="Bin Count (Seaborn)", min=1, max=100, value=10 )

    ui.input_checkbox_group(
        id="selected_species_list",
        label="Various Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
        inline=False,
    )

    ui.hr()

    ui.a( "Source code on Github", href="https://github.com/diamondhelm/cintel-02-data", target="_blank")

with ui.layout_columns(): 
    with ui.card(full_screen=True):
        ui.card_header("Plotly of Penguin Species")
        @render.data_frame
        def table():
            return render.DataTable(data=filtered_data())

    with ui.card(full_screen=True):
        ui.card_header( "Grid of Penguin Species")
        @render.data_frame
        def grid():
            return render.DataGrid(data=filtered_data())

    with ui.layout_columns():
        with ui.card(full_screen=True):
            ui.card_header("Plotly Histogram:Penguins by Body Mass")
        @render_plotly
        def plot1():
            return px.histogram(filtered_data(), x="body_mass_g", color="species", nbins=input.plotly_bin_count())
            
    with ui.card(full_screen=True):
        ui.card_header("Penguins by Flipper Length")
        @render.plot
        def plot2():
            return sns.histplot(data=filtered_data(), x="flipper_length_mm", hue="species", bins=input.seaborn_bin_count())

with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Various Species")
    @render_plotly
    def plotly_scatterplot():
        return px.scatter(data_frame=filtered_data(), x="body_mass_g", y="bill_length_mm", color="species", hover_name="island", symbol="sex")

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    return penguins_df
