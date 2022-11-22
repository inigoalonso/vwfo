"""
# Value Weighted Filtered Outdegree (VWFO) App
This app describes the Value Weighted Filtered Outdegree (VWFO) metric and it lets you play with it.
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Set page properties, if not made before
try:
    st.set_page_config(layout="wide", page_title="Value Weighted Filtered Outdegree (VWFO) App")
except:
    pass

from helpers.app_helpers import calculate_vwfo


with st.sidebar:
    st.header("Inputs")
    uploaded_files_1 = st.file_uploader("Set of designss", type="csv", accept_multiple_files=False)
    if uploaded_files_1 is not None:
        df_designs = pd.read_csv(uploaded_files_1)
        #st.dataframe(df_designs)
        scenarios = df_designs['scenario'].unique()
        designs = df_designs['design'].unique()
    expected_files = []
    if uploaded_files_1 is not None:
        for i, scenario in enumerate(scenarios):
            if i < len(scenarios)-1:
                expected_files.append(f"{scenario}_{scenarios[i+1]}.csv")
        uploaded_files_2 = st.file_uploader(f"Expected files: {expected_files}", type="csv", accept_multiple_files=True)


st.title("VWFO app")
st.caption("Calculate the VWFO of a set of designs")
with st.expander("Help"):
    # Help section
    mkd = """
    This app allows you calculate the VWFO of a set of designs.
    For example, if you provide:
    * Set of Designs: `designs.csv`
    * Available transtions between desings: `s1_s2.csv`, `s2_s3.csv`
    You will get the following file on the output:
    * `designs_vwfo.csv`
    You can set specific encodings and separators for inputs and outputs (or infer them for the inputs).
    * **Inputs 1**: 
        * CSV file: upload the CSV file with your set of designs. 
        * Encoding: select the encoding of the CSV files. If you don't know, leave it as it is.
        * Separator: select the separator of the CSV files. If you don't know, leave it as it is.
    * **Inputs 2**: 
        * CSV file(s): upload the CSV files with the available transitions between scenarios. You can upload multiple files at once.
        * Encoding: select the encoding of the CSV files. If you don't know, leave it as it is.
        * Separator: select the separator of the CSV files. If you don't know, leave it as it is.
    * **Output Configuration**: 
        * Date: Select the date you want to use for the output file (as `yyyymmdd`).
        * Encoding: select the encoding for the csv files.
        * Separator: select the separator for the csv files. 
    * **Outputs**: 
        * A zip file containing the csv file.
    """
    st.markdown(mkd)
message_missing_designs = st.empty()

# Display the input for designs and their surplus values
if uploaded_files_1 is not None:
    st.markdown(f"#### {len(designs)} Designs and {len(scenarios)} Scenarios")
    st.caption(f"Detected {len(designs)} designs {designs} and {len(scenarios)} scenarios {scenarios}")

    c = alt.Chart(df_designs).mark_line().encode(
        x='scenario:N',
        y='sv:Q',
        color='design:N'
    )
    st.altair_chart(c, use_container_width=True)

    message_missing_transitions = st.empty()
    if 'uploaded_files_2' in locals():
        if uploaded_files_2 != []:
            # Display the inputs for transitions
            st.markdown("#### Design transitions")
            st.caption("Available transitions between designs")

            # Display outputs
            st.markdown("#### Output")
            c1, c2 = st.columns([1,1])
            current_scenario = c1.selectbox("Select current scenario", options=scenarios)
            following_scenario = c2.selectbox("Select following scenario", options=np.delete(scenarios, np.where(scenarios==current_scenario)))
    
            selected_design = c1.selectbox("Select design", options=designs)
            selected_design_sv = df_designs[df_designs['design'] == selected_design]['sv'].values
            selected_design_current_sv = df_designs[(df_designs['design'] == selected_design) & (df_designs['scenario'] == current_scenario)]['sv'].values[0]
            selected_design_following_sv = df_designs[(df_designs['design'] == selected_design) & (df_designs['scenario'] == following_scenario)]['sv'].values[0]
            #st.write(f"Surplus value of {selected_design} for scenario {current_scenario}: {selected_design_current_sv}")
            #st.write(f"Surplus value of {selected_design} for scenario {following_scenario}: {selected_design_following_sv}")

            for file in uploaded_files_2:
                if file.name == f"{current_scenario}_{following_scenario}.csv":
                    df_transition = pd.read_csv(file)
                    df_transition.set_index('design', inplace=True)
            #st.dataframe(df_transition)

            following_designs = [k for k,v in df_transition.loc[selected_design].to_dict().items() if v == 1]
            #st.write(f"Following designs: {following_designs}")
            following_designs_sv = df_designs[(df_designs['design'].isin(following_designs)) & (df_designs['scenario'] == following_scenario)]['sv'].values
            #st.write(f"Surplus values of following designs: {following_designs_sv}")

            c2.write(f"VWFO of design {selected_design}: {calculate_vwfo(len(designs), selected_design_current_sv, following_designs_sv)}")

            for design in designs:
                design_current_sv = df_designs[(df_designs['design'] == design) & (df_designs['scenario'] == current_scenario)]['sv'].values[0]
                design_following_sv = df_designs[(df_designs['design'] == design) & (df_designs['scenario'] == following_scenario)]['sv'].values[0]
                following_designs = [k for k,v in df_transition.loc[design].to_dict().items() if v == 1]
                following_designs_sv = df_designs[(df_designs['design'].isin(following_designs)) & (df_designs['scenario'] == following_scenario)]['sv'].values
                st.write(f"VWFO of design {design}: {calculate_vwfo(len(designs), design_current_sv, following_designs_sv)}")



if 'uploaded_files_2' in locals():
    if uploaded_files_2 == []:
        # If something is not working, stop here...
        message_missing_transitions.error("Upload transitions files to continue")
if uploaded_files_1 is None:
    # If something is not working, stop here...
    message_missing_designs.error("Upload designs file to continue")