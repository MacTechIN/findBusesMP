import streamlit as st

i1 = st.button("button 1")
st.write("value:", i1)

i2 = st.checkbox("reset button")


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

