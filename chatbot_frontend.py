import streamlit as st
import requests
from PIL import Image
import io

st.header("AI-Based Chat and Image Generation")

col1,col2=st.columns([6,1])
with col1:
    select=st.selectbox("Select",["Chat💬","Image Generation🖼️"],label_visibility="collapsed")

with col2:
    if st.button("Reset🔄"):
        response = requests.delete("http://127.0.0.1:8000/clear-history")

        if response.status_code == 200:

            if "messages" in st.session_state:
                st.session_state.messages = []

user_input= st.chat_input("Type your message...")

if select =="Chat💬":

    with st.expander("Upload file📁"):
        file_uploader = st.file_uploader("upload")

        if user_input and file_uploader:
            response = requests.post("http://127.0.0.1:8000/upload-file",data={"question":user_input},files={"file":file_uploader})
            
            if response.status_code == 200:
                chat = response.json()
                st.write("👤 User:", chat["user"])
                st.write("🤖 Bot:", chat["bot"])

        elif user_input:
            response = requests.post("http://127.0.0.1:8000/chat",json={"question":user_input})
            if response.status_code == 200:
                chat = response.json()
                st.write("👤 User:", chat["User"])
                st.write("🤖 Bot:" ,chat["Bot"])
        

    if st.button("History📜"):
        response = requests.get("http://127.0.0.1:8000/history")

        if response.status_code == 200:
            history = response.json()
            
            if not history:
                st.info("🕘 No chat history available yet.")
            else:
                for chat in history:
                    st.write("👤 User:", chat["question"])
                    st.write("🤖 Bot:", chat["answer"])
        

if select=="Image Generation🖼️":

    if user_input:
        response = requests.post("http://127.0.0.1:8000/generate-image",json={"prompt":user_input})

        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            st.image(img, caption="Generated Image", width=500)
       
            st.download_button(
                label="⬇️ Download Image",
                data=response.content,
                file_name="generated_image.png",
                mime="image/png")
        else:
            st.error("Error")







