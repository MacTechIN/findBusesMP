import streamlit as st

i1 = st.button("button 1")
st.write("value:", i1)

i2 = st.checkbox("reset button")


import streamlit as st

st.title("Streamlit Test")
input_user_name = st.text_input(label="User Name", value="")

checkbox = st.checkbox('agree')
btn_clicked = st.button("Confirm", key='confirm_btn', disabled=(checkbox is False))

if btn_clicked:
    con = st.container()
    con.caption("Result")
    con.write(f"Hello~ {str(input_user_name)}")