import os
import time
import requests
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from PIL import Image


STYLES = {
    "candy": "candy",
    "composition 6": "composition_vii",
    "feathers": "feathers",
    "la_muse": "la_muse",
    "mosaic": "mosaic",
    "starry night": "starry_night",
    "the scream": "the_scream",
    "the wave": "the_wave",
    "udnie": "udnie",
}


with open(os.path.join(os.getcwd(),'config.yaml')) as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Hello!  Welcome *{st.session_state["name"]}*')
    #st.title('Some content')
    st.set_option("deprecation.showfileUploaderEncoding", False)
    st.title("Style transfer web app")
    image = st.file_uploader("Choose an image")
    style = st.selectbox("Choose the style", [i for i in STYLES.keys()])

    if st.button("Style Transfer"):
        if image is not None and style is not None:
            files = {"file": image.getvalue()}
            res = requests.post(f"http://backend:8080/{style}", files=files)
            img_path = res.json()
            image = Image.open(img_path.get("name"))
            st.image(image)

            displayed_styles = [style]
            displayed = 1
            total = len(STYLES)

            st.write("Generating other models...")

            while displayed < total:
                for style in STYLES:
                    if style not in displayed_styles:
                        try:
                            path = f"{img_path.get('name').split('.')[0]}_{STYLES[style]}.jpg"
                            image = Image.open(path)
                            st.image(image, width=500)
                            time.sleep(1)
                            displayed += 1
                            displayed_styles.append(style)
                        except:
                            pass

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')

# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{name}*')
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username/password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')