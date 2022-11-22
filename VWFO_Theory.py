"""
# Value Weighted Filtered Outdegree (VWFO)
This app describes the Value Weighted Filtered Outdegree (VWFO) metric and it lets you play with it.
"""

import streamlit as st

# Set wide display, if not done before
try:
    st.set_page_config(layout="wide", page_title="Value Weighted Filtered Outdegree (VWFO)")
except:
    pass

st.title('Value Weighted Filtered Outdegree (VWFO)')

st.header('Definition')

st.latex(r'''
    {VWFO}^{k}_{i} =
    \frac {1}{N-1} \times 
    \sum_{j=1}^{N-1} \left[ sign \left( {SV}^{k+1}_{j} - {SV}^{k+1}_{i} \right) \times {Arc}^{k}_{i,j} \right]
    ''')

st.markdown('''
Where:

$N$				Number of designs

$i$				Current design

$j$				Target design

$k$				Current scenario

$k+1$			Following scenario

$SV$			Surplus Value

$Arc_{i,j}^{k}$	Arc
''')
