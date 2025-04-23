import time
import streamlit as st


def relevant_profiles(response, number_of_profiles):
        for i in range(number_of_profiles):

            profile_name = response["context"][i].metadata["name"]
            role = response["context"][i].metadata["role"]
            certificates = response["context"][i].metadata["certificates"]
            technologies = response["context"][i].metadata["technologies"]
            seniority = response["context"][i].page_content.split("-")[2]


            st.subheader(f"Recommended Profiles -> ")
            st.info(f"✅ Name {profile_name}  \n 👩‍💻 Role: {role}  \n 📌 Certificates: {certificates}  \n 📝 Technologies: {technologies} \n\n 👩‍💻{seniority}")

def selectbox_styling():

    st.markdown(
        """
        <style>
        div[data-testid="stNumberInput"] {
            width: 660px !important; /* Adjust width as needed */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
            """
            <style>
            div[data-testid="stSelectbox"] {
                width: 660px !important; /* Adjust width as needed */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(
            """
            <style>
            div[data-testid="stAlert"] {
                width: 660px !important; /* Adjust width as needed */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    
def response_generator(response):
    for word in response.split(" "):
        yield word + " "
        time.sleep(0.14)
    
