import time
# import streamlit as st
from explainable_agent import ExplanationAgent

def relevant_profiles(api_key, project_details, response, number_of_profiles):
        explainable_ai_agent = ExplanationAgent(api_key)
        specific_skill_relevant_profiles = []
        for i in range(number_of_profiles):
            
            profile_name = response[i][0].metadata.get("name")
            role = response[i][0].metadata.get("role")
            certificates = response[i][0].metadata.get("certificates")
            technologies = response[i][0].metadata.get("technologies")
            languages_spoken = response[i][0].metadata.get("languages_spoken")
            profile_description = response[i][0].metadata.get("description")
            seniority = response[i][0].metadata.get("seniority")
            similarity_score = response[i][1]

            profile_details = f"""Role: {role}-Technologies: {technologies}-Candidate description: {profile_description}"""
            explanation, score = explainable_ai_agent.explain_match(project_details, profile_details, similarity_score)
            
            specific_skill_relevant_profiles.append({
                "profile_name": profile_name,
                "role":role,
                "certificates":certificates,
                "technologies":technologies,
                "languages_spoken":languages_spoken,
                "profile_description":profile_description,
                "seniority":seniority,
                "sim_score": score,
                "explanation": explanation
            })

        return specific_skill_relevant_profiles 


# def relevant_profiles(response, number_of_profiles):
#         specific_skill_relevant_profiles = []
#         # print("Score",sim_response[0][1])
#         # print("Score",sim_response[0][0].metadata.get("technologies"))
#         for i in range(number_of_profiles):

#             profile_name = response["context"][i].metadata["name"]
#             role = response["context"][i].metadata["role"]
#             certificates = response["context"][i].metadata["certificates"]
#             technologies = response["context"][i].metadata["technologies"]
#             languages_spoken = response["context"][i].metadata["languages_spoken"]
#             profile_description = response["context"][i].metadata["description"]
#             seniority = response["context"][i].metadata["seniority"]
#             # seniority = response["context"][i].page_content.split("-")[2]

#             # print(f"✅ Name {profile_name}  \n 👩‍💻 Role: {role}  \n 📌 Certificates: {certificates}  \n 📝 Technologies: {technologies} \n\n 👩‍💻{seniority}")
#             # st.subheader(f"Recommended Profiles -> ")
#             # st.info(f"✅ Name {profile_name}  \n 👩‍💻 Role: {role}  \n 📌 Certificates: {certificates}  \n 📝 Technologies: {technologies} \n\n 👩‍💻{seniority}")
#             specific_skill_relevant_profiles.append({
#                 "profile_name": profile_name,
#                 "role":role,
#                 "certificates":certificates,
#                 "technologies":technologies,
#                 "languages_spoken":languages_spoken,
#                 "profile_description":profile_description,
#                 "seniority":seniority
#             })

#         return specific_skill_relevant_profiles 

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
    
