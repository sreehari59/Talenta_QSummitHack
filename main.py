from flask import Flask, jsonify, request
from rag import RagModel
from utils import relevant_profiles, weighted_relevant_profiles, sort_by_total_score, build_company_email_prompt, build_candidate_email_prompt, generate_email, send_email
from flask_cors import CORS
from openai import OpenAI
from dotenv import dotenv_values
config = dotenv_values(".env")

app = Flask(__name__)
CORS(app)

@app.route('/recommend_candidates', methods=['POST'])
def recommend_candidates():
    data = request.get_json()

    api_key = config["OPEN_AI_KEY"]
    embedding_model = config["OPEN_AI_EMBEDDING_MODEL"]
    model = config["OPEN_AI_MODEL_NAME"]

    rag = RagModel(api_key, config["QDRANT_API_KEY"], config["QDRANT_URL"], 
                            config["QDRANT_COLLECTION_NAME"], embedding_model, model, 5)

    project_name= data["projectApplication"]["projectDetails"]["projectName"]
    project_description = data["projectApplication"]["projectDetails"]["description"]
    total_number_of_requirements = len(data["projectApplication"]["projectDetails"]["requirements"])
    recommended_candidates = []
    print("-----------------------")
    print("project_name",project_name)
    print("project_description",project_description)
    print("Total Number of unique positions:", total_number_of_requirements)
    for i in range(total_number_of_requirements):
        if len(data["projectApplication"]["projectDetails"]["requirements"][i]) < 2:
            skill_required = data["projectApplication"]["projectDetails"]["requirements"][i]["skill"]
            amount_required = 1
            recommended_seniority = ""
        else:
            skill_required = data["projectApplication"]["projectDetails"]["requirements"][i]["skill"]
            amount_required = data["projectApplication"]["projectDetails"]["requirements"][i]["amount"]
            recommended_seniority = data["projectApplication"]["projectDetails"]["requirements"][i]["recommendedSeniority"]
        print("******************")
        print("skill_required",skill_required)
        print("amount_required",amount_required)
        print("recommended_seniority",recommended_seniority)

        project_details = f"""
        Project Name: {project_name}-Project Description: {project_description}-Required Skill: {skill_required}-Recommended Seniority: {recommended_seniority}
        """
        response = rag.retrieve_data(project_details, amount_required, False)
        recommended_candidates.append(relevant_profiles(api_key, project_details, response, amount_required + 2))

    return jsonify(recommended_candidates)

@app.route('/weighted_recommend_candidates', methods=['POST'])
def weighted_recommend_candidates():
    data = request.get_json()

    api_key = config["OPEN_AI_KEY"]
    embedding_model = config["OPEN_AI_EMBEDDING_MODEL"]
    model = config["OPEN_AI_MODEL_NAME"]
    number_of_profiles_required = int(config["NUMBER_OF_PROFILES_REQUIRED"])

    rag = RagModel(api_key, config["QDRANT_API_KEY"], config["QDRANT_URL"], 
                            config["QDRANT_COLLECTION_NAME"], embedding_model, model, number_of_profiles_required)

    project_name= data["projectApplication"]["projectDetails"]["projectName"]
    project_description = data["projectApplication"]["projectDetails"]["description"]
    total_number_of_requirements = len(data["projectApplication"]["projectDetails"]["requirements"])
    initial_recommended_candidates = []
    print("-----------------------")
    print("project_name",project_name)
    print("project_description",project_description)
    print("Total Number of unique positions:", total_number_of_requirements)
    for i in range(total_number_of_requirements):
        if len(data["projectApplication"]["projectDetails"]["requirements"][i]) < 2:
            skill_required = data["projectApplication"]["projectDetails"]["requirements"][i]["skill"]
            amount_required = 1
            recommended_seniority = ""
        else:
            skill_required = data["projectApplication"]["projectDetails"]["requirements"][i]["skill"]
            amount_required = data["projectApplication"]["projectDetails"]["requirements"][i]["amount"]
            recommended_seniority = data["projectApplication"]["projectDetails"]["requirements"][i]["recommendedSeniority"]
        print("******************")
        print("skill_required",skill_required)
        print("amount_required",amount_required)
        print("recommended_seniority",recommended_seniority)

        project_details = f"""
        Project Name: {project_name}-Project Description: {project_description}-Required Skill: {skill_required}-Recommended Seniority: {recommended_seniority}
        """
        response = rag.retrieve_data(project_details, amount_required, False)
        location = data["projectApplication"]["projectDetails"]["location"]
        initial_recommended_candidates.append(weighted_relevant_profiles(api_key, project_details, response,
                                                                        amount_required + number_of_profiles_required,
                                                                        project_description, skill_required,
                                                                        location, recommended_seniority))

    sorted_recommended_candidates = sort_by_total_score(initial_recommended_candidates)    

    return jsonify(sorted_recommended_candidates)

@app.route("/email_sender", methods=["POST"])
def postME():
    client = OpenAI(
            api_key=os.environ.get("OPEN_AI_KEY"),
        )
    data = request.get_json()
    company_name = data['project']['projectApplication']['businessDetails']['name']
    contact_name = data['project']['projectApplication']['businessDetails']['contactPerson']['name']
    project_name = data['project']['projectApplication']['projectDetails']['projectName']
    project_description = data['project']['projectApplication']['projectDetails']['description']
    project_requirements = data['project']['projectApplication']['projectDetails']['requirements']
    project_skills = [project_requirement['skill'] for project_requirement in project_requirements]

    candidates_list = data['candidates']

    # Send to the client
    prompt = build_company_email_prompt(company_name, contact_name, project_name, project_skills, candidates_list)
    # print(prompt)
    subject, body = generate_email(prompt)
    send_email('hackathon.hyw.2025@gmail.com', subject, body)
    
    # Send to the consultants
    prompt = build_candidate_email_prompt(company_name, contact_name, project_name, project_description, candidates_list)
    # print(prompt)
    subject, body = generate_email(prompt)
    send_email('hackathon.hyw.2025@gmail.com', subject, body)
    
    return jsonify({"message": "Emails sent successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)