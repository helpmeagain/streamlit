import streamlit as st
import numpy as np
import pandas as pd
import time

df = pd.DataFrame({
    'first column': [1, 2, 3 ,4],
    'second column': [10, 20, 30, 40]
})

df
st.write("First attempt at using data to create a table")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=['a', 'b', 'c'])
st.bar_chart(chart_data)

chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [100, 100] + [-6.600, -39.055],
    columns=['lat', 'lon'])
st.map(map_data)


x= st.slider('x')
st.write(x, 'squared is', x * x)
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
        np.random.randn(20,3),
        columns=['a', 'b', 'c'])
   
    chart_data

if st.checkbox('Show map'):
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [10, 10] + [-19.890, -43.967],
        columns=['lat', 'lon'])
   
    st.map(map_data)
   
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home Phone', 'Mobile phone')
)

add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i+1}')
    bar.progress(i + 1)
    time.sleep(0.1)
