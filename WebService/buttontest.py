import streamlit as st

i1 = st.button("button 1")
st.write("value:", i1)

i2 = st.checkbox("reset button")


<<<<<<< HEAD
import streamlit as st

st.title("Streamlit Test")
input_user_name = st.text_input(label="User Name", value="")

checkbox = st.checkbox('agree')
btn_clicked = st.button("Confirm", key='confirm_btn', disabled=(checkbox is False))

if btn_clicked:
    con = st.container()
    con.caption("Result")
    con.write(f"Hello~ {str(input_user_name)}")
=======
st.title("Yes or No Decision")

my_add = "경기도 수원시 "

my_add = st.text_input('주소를 넣어주세요', '경기도 수원시 ')

if st.button("Yes"):
    st.write( f"당신의 주소는 {my_add}이 시군요")
    st.write("다음 스테이지 ")
    if st.button("No"):
        st.write("You clicked 'No'")
        if st.button("Yes2"):
            st.write(f"당신의 주소는 {my_add}이 시군요")
            st.write("다음 스테이지 ")

>>>>>>> 9ac516b8839246b7ceb282f7f5465d1d291425c4
