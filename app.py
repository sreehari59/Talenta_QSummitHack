import streamlit as st
import pandas as pd
from dotenv import dotenv_values
import os
from rag import RagModel
from utils import response_generator, selectbox_styling, relevant_profiles
import warnings
warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

selectbox_styling()
config = dotenv_values(".env")
# new_df = pd.read_csv(config["NEW_DATA"])
# new_df.loc[new_df['gender'].isin(['x', 'v', 'u']), 'gender'] = 'o'
# new_df['risk_groups'] = new_df['risk_groups'].fillna("None")
# new_df["Patientenname_ageGroup"] = new_df["Patientenname"] + " : " + new_df["age_group"] + " : " + new_df["risk_groups"]

# Main Ttile
st.markdown("""
    <div style='text-align: center;'>
    <h1>Talenta</h1>
        <h2>Staff Management Platform</h2>
    </div>
""", unsafe_allow_html=True)


# Retrieves relevant ticket
def Reco_Sys():
    project_details = """
    Project Name: Blockchain-Based Financial Reporting
    Project Description: FinanceCorp International is embarking on a transformative project to incorporate blockchain technology into financial reporting practices. The initiative will streamline reconciliation processes and provide immutable records for audit purposes. The use of smart contracts will automate compliance checks, reducing human error and enhancing procedural speed. Security and privacy are essential, with the platform ensuring encryption standards that adhere to financial regulatory requirements. Transparency and clarity in financial data presentation are priorities, with user-friendly interfaces aimed at accountants and auditors alike. Ultimately, the project aims to set new industry benchmarks for efficiency and reliability in financial reporting.
    Total Number of requirements: 1 {'skill': 'Blockchain Development', 'amount': 1} 
            """
    # project_details = st.text_input("Project Details")

    df = pd.read_json("data/profiles copy.json")
    project_name= df["projectApplication"][2]["projectDetails"]["projectName"]
    project_description = df["projectApplication"][2]["projectDetails"]["description"]
    st.info(f"""Project Name: {project_name} \n\n\n Project Description: {project_description}""")

    
    print("Total Number of unique positions:", len(df["projectApplication"][0]["projectDetails"]["requirements"]))
    # for i in range(len(df["projectApplication"][0]["projectDetails"]["requirements"])):
    #     st.info(df["projectApplication"][0]["projectDetails"]["requirements"][i])
    #     break

    
    api_key = config["OPEN_AI_KEY"]
    embedding_model = config["OPEN_AI_EMBEDDING_MODEL"]
    model = config["OPEN_AI_MODEL_NAME"]
    rag = RagModel(api_key, config["QDRANT_API_KEY"], config["QDRANT_URL"], 
                        config["QDRANT_COLLECTION_NAME"], embedding_model, model, 5)
    

    
    response = rag.retrieve_data(project_details, 5, False)
    print(response["answer"])
    print(response)

    relevant_profiles(response, 5)
    # number_of_patients = st.number_input("Number of Relevant Similar Patients", value=3)
    # vaccinated_patients = st.checkbox("Tick to retrieve details of only vaccinated patients")
    
    # patient_detail_flag = False
    # patient_assistance_flag = False
    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     if st.button("Patient Details"):
    #         patient_detail_flag = True
            
    # with col3:
    #     if st.button("🤖 AI Patient Assistance"):
    #         patient_assistance_flag =True
            

    # if patient_detail_flag:
    #     filtered_df = new_df[new_df["Patientenname_ageGroup"] == name_of_patient] 
    #     df_melted = filtered_df.melt(var_name="Field", value_name="Value")
    #     st.write(df_melted)

    # if patient_assistance_flag:
    #     filtered_df = new_df[new_df["Patientenname_ageGroup"] == name_of_patient] 
    #     df_melted = filtered_df.melt(var_name="Field", value_name="Value")
    #     st.write(df_melted)
    #     filtered_df.reset_index(inplace=True, drop=True)
      
    #     user_query = f"""KV Region: {filtered_df["kvregion"][0]}
    #                     Gender: {filtered_df["gender"][0]} Age Group: {filtered_df["age_group"][0]} 
    #                     Risk Group: {filtered_df['risk_groups'][0]}"""

        # st.info(f"""📌Patientenname: {filtered_df["Patientenname"][0]} {user_query}""")

    #     api_key = config["TOGETHER_AI_API_KEY"]
    #     embedding_model = config["HUGGING_FACE_EMBEDDING_MODEL"]
    #     model = config["TOGETHER_AI_MODEL_NAME"]

    #     rag = RagModel(api_key, config["QDRANT_API_KEY"], config["QDRANT_URL"], 
    #                     config["QDRANT_COLLECTION_NAME"], embedding_model, model, number_of_patients)
        
    #     response = rag.retrieve_data(user_query, vaccinated_patients)
    #     st.header("🔗 Relevant Past Patient Vaccination Information")

    #     with st.expander("🔗 Relevant Past Similar Patient"):
    #         relevant_ticket_details(response, number_of_patients)

    #     resolution = response["answer"]
    #     with st.chat_message("assistant"):
    #         st.write_stream(response_generator(resolution))

    #     if st.button("Scheduling Agent"):
    #         st.info("Scheduling in Progress....")
            

# To upload new documents 
def Process_Docs():
    uploaded_file = st.file_uploader(
                        "Upload the file", 
                        type = ["csv", "xlsx", "json"],
                        accept_multiple_files=False
                        )
    if st.button("Process Document"):
        if uploaded_file is not None:
            if ".csv" in uploaded_file.name:
                uploaded_df = pd.read_csv(uploaded_file)
            elif ".xlsx" in uploaded_file.name:
                uploaded_df = pd.read_excel(uploaded_file)
            elif ".json" in uploaded_file.name:
                uploaded_df = pd.read_json(uploaded_file)
            
            st.write(uploaded_df)
            api_key = config["OPEN_AI_KEY"]
            embedding_model = config["OPEN_AI_EMBEDDING_MODEL"]
            model = config["OPEN_AI_MODEL_NAME"]

            rag = RagModel(api_key, config["QDRANT_API_KEY"], config["QDRANT_URL"], 
                            config["QDRANT_COLLECTION_NAME"], embedding_model, model)
            
            collection_name = rag.upload_data(uploaded_df)

            st.write("Document Processed Successfully")
            st.write("Uploded the data in :", collection_name)
    
pg = st.navigation([st.Page(Reco_Sys), st.Page(Process_Docs)])
pg.run()

# For the foter
st.caption("Powered by Agentic AI 🚀")