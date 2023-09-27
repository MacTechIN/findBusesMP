import streamlit as st

st.title("Yes or No Decision")

if st.button("Yes"):
    st.write("You clicked 'Yes'")
elif st.button("No"):
    st.write("You clicked 'No'")
