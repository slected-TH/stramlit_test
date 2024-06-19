import streamlit as st
from PIL import Image

#사이드 바 화면
st.sidebar.header("로그인")
user_id = st.sidebar.text_input("아이디 입력",value='',max_chars=15)
user_password = st.sidebar.text_input("패스워드 입력",value='',type='password')

if user_id=="1234"and user_password == '1234' :
    st.sidebar.header("그림목록")
    sel_options=['','진주 귀걸이를 한 소녀','별이 빛나는 밤','절규','생명의 나무','월하정인']
    user_opt = st. sidebar.selectbox("좋아하는 작품은?",sel_options,index=0)
    st.sidebar.write("***선택한 그림은 ",user_opt)

    #메인 화면
    st.subheader("Main")
    image_files=['welcome.jpg','Vermeer.png','Gogh.png','Munch.png','Klimt.jpg','ShinYoonbok.png']
    sel_index = sel_options.index(user_opt)
    imag_file = image_files[sel_index]
    img_local = Image.open(f"img/{imag_file}")
    st.image(img_local,caption=user_opt)
