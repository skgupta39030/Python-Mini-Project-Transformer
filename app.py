import sqlite3
import streamlit as st
import pandas as pd
from PIL import Image
from transformers import pipeline

# Security
# passlib,hashlib,bcrypt,scrypt
import hashlib


@st.cache(allow_output_mutation=True)
def load_qa_model():
    model = pipeline("question-answering")
    return model


qa = load_qa_model()


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB Management
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions


def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',
              (username, password))
    conn.commit()


def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',
              (username, password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


side = st.sidebar
menu = ["Home", "Login", "SignUp"]
choice = st.sidebar.selectbox("Menu", menu)


if choice == "Home":
    sideBarImage = Image.open("./sidebar.png")
    side.image(sideBarImage, width=280)
    st.markdown(f"<html><body><h1 style='color:tomato;font-size: 250%;font-family: Arial, Helvetica, sans-serif; margin-top:0%'>Welcome to Get Your Answer!!!</h1></body></html>", unsafe_allow_html=True)
    st.subheader(
        " AI will answers to your questions about your passages/articles.")
    st.write(" About the model: Transformer is a deep learning model that adopts the mechanism of attention, differentially weighing the significance of each part of the input data. It is used primarily in the field of natural language processing (NLP) and in computer vision (CV).")

    img = Image.open("./title_image.png")

    col1, col2, col3 = st.columns([1, 6, 1])
    col1.write("")
    col2.image(img, width=500)
    col3.write("")


elif choice == "Login":

    st.markdown(f"<html><body><h1 style='color:tomato; text-align:center; font-size: 250%;font-family: Arial, Helvetica, sans-serif; margin-top:0%'>Hello people, login to get started!!!</h1></body></html>", unsafe_allow_html=True)

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.checkbox("Login"):
        #result = login_user(username,password)
        # if password == '12345':
        create_usertable()
        hashed_pswd = make_hashes(password)

        result = login_user(username, check_hashes(password, hashed_pswd))

        if result:
            st.sidebar.success("Logged In as {}".format(username))
            st.markdown(f"<html><body><h1 style=' text-align:center; font-size: 150%;font-family: Arial, Helvetica, sans-serif; margin-top:0%'>Ask Questions about your Article\n</h1></body></html>", unsafe_allow_html=True)
            # st.title("Ask Questions about your Article")
            sentence = st.text_area('Please paste your article :', height=30)
            question = st.text_input("Questions from this article?")
            button = st.button("Get me Answer")
            # max = st.sidebar.slider('Select max', 50, 500, step=10, value=150)
            # min = st.sidebar.slider('Select min', 10, 450, step=10, value=50)
            # do_sample = st.sidebar.checkbox("Do sample", value=False)
            with st.spinner("Discovering Answers.."):
                if button and sentence:
                    answers = qa(question=question, context=sentence)
                    st.write(answers['answer'])

        else:
            st.sidebar.warning("Incorrect Username/Password")

elif choice == "SignUp":
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')

    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user, make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")
