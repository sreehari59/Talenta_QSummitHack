from agents.explainable_agent import ExplanationAgent
from agents.geo_lang_scorer import GeoLangScoringAgent
from agents.description_scorer import DescriptionScoringAgent
from agents.seniority_scorer import SeniorityScoringAgent
from agents.skills_scorer import SkillScoringAgent
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Tuple
import smtplib
import os
import json
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get("OPEN_AI_KEY"),
)

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

def weighted_relevant_profiles(api_key, project_details, response, number_of_profiles,
                               project_description, skill_required,
                               location, recommended_seniority):
        # explainable_ai_agent = ExplanationAgent(api_key)

        # Description Scorer
        desc_scorer = DescriptionScoringAgent(api_key)
        
        # Seniority Scorer
        seniority_scorer = SeniorityScoringAgent(api_key)
        
        # Location Language Scorer
        geo_lang_scorer = GeoLangScoringAgent(api_key)

        # Skill Scorer
        skill_scorer = SkillScoringAgent(api_key)

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
            
            
            description_score, description_explanation = desc_scorer.description_scoring_func(project_description, profile_description)

            # Seniority Scorer
            seniority_score, seniority_explanation = seniority_scorer.seniority_scoring_func(recommended_seniority, seniority)

            # Location Language Scorer
            geo_lang_score, geo_lang_explanation = geo_lang_scorer.geo_lang_scoring_func(location, languages_spoken)

            # Skill Scorer
            skill_score, skills_explanation = skill_scorer.skills_scoring_func(skill_required, technologies,
                                                       certificates)
            total_score = (int(description_score)*2) + (int(seniority_score)*2) + (int(geo_lang_score)*2) + (int(skill_score)*2) + (float(similarity_score)*30)
            print("total_score",total_score)
            
            specific_skill_relevant_profiles.append({
                "profile_name": profile_name,
                "role":role,
                "certificates":certificates,
                "technologies":technologies,
                "languages_spoken":languages_spoken,
                "profile_description":profile_description,
                "seniority": seniority,
                "description_score": description_score,
                "description_explanation": description_explanation, 
                "seniority_score": seniority_score,
                "seniority_explanation": seniority_explanation,
                "geo_lang_score": geo_lang_score,
                "geo_lang_explanation": geo_lang_explanation,
                "skill_score": skill_score,
                "skills_explanation": skills_explanation,
                "total_score": total_score
            })

        return specific_skill_relevant_profiles 

def sort_by_total_score(data):
    sorted_data = []  
    for inner_list in data:
        if not isinstance(inner_list, list):
            sorted_data.append(inner_list) 
            continue

        # Sort the inner list using the total_score as the key, in descending order
        sorted_inner_list = sorted(inner_list, key=lambda x: x.get('total_score', 0), reverse=True)
        sorted_data.append(sorted_inner_list) 

    return sorted_data

def build_company_email_prompt(
    company_name: str, contact_name: str, project_name: str, project_skills: List[str],
    candidates_per_requirements: List[List[Dict]], scheduling_link: str = "https://your-scheduling-link.com",
) -> str:
    candidates_text = ""
    for skill, candidates in zip(project_skills, candidates_per_requirements):
        candidates_text += f"The following consultants are assigned for the required skill: {skill}\n"
        candidates_text += "\n".join(
            f"- {c['profile_name']} ({c['seniority']} {c['role']}): {c['profile_description']}"
            for c in candidates
        )

    prompt = f"""
        You are writing an email to the contact person at a company.

        Contact name: {contact_name}
        Company name: {company_name}
        Project name: {project_name}

        Context:
        The company has requested consultant support for a project. You are now presenting a curated shortlist of recommended candidates for their consideration. Each candidate was selected based on alignment with the project's specific skill requirements.
        
        Here are the selected candidates:
        {candidates_text}

        Write a professional email with:
        - A subject line on the first line only. Do **not** add “Subject:” or any label. Just write the subject text. (e.g. “Recommended Candidates for [Project Name]”)
        - A greeting using the contact name
        - A brief introduction referencing the project and purpose
        - A short, readable summary of the recommended candidates and their assigned role
        - A polite closing

        At the end of the email, include the following sentence:
        "Please schedule a short alignment interview using the following link: {scheduling_link}"

        At the very end of the email, sign off with:
        Best regards,
        Theo Wong – Senior Manager

        Please write the entire email in plain text only. Do not use Markdown or any special formatting (e.g., asterisks, bold, or italics). Do not add any details not included above.
        """
    return prompt


def build_candidate_email_prompt(
    company_name: str, contact_name: str, project_name: str, project_description: str, 
    candidates_per_requirements: List[List[Dict]], scheduling_link="https://your-scheduling-link.com",
) -> str:
    lines = []
    for candidates in candidates_per_requirements:
        lines.extend(
            f"- {c['profile_name']} ({c['role']})"
            for c in candidates
        )
    candidates_text = "\n".join(lines)

    prompt = f"""
        You are a professional consultant coordinator writing an email to a group of consultants from your firm.

        Context:
        You are notifying selected consultants that they’ve been chosen to participate in a client project. The goal is to inform, motivate, and briefly outline the project.

        Client company: {company_name}
        Client contact person: {contact_name}
        Project name: {project_name}
        Project description: {project_description}

        The following candidates have been selected for this project:
        {candidates_text}

        Write a professional email with:
        - A subject line on the first line only. Do **not** add “Subject:” or any label. Just write the subject text. (e.g., “You’ve Been Assigned to {project_name}”)
        - A warm greeting to the consultants as a group
        - A brief paragraph announcing their selection and acknowledging their skills
        - A short summary of the project and the client
        - A motivational tone that communicates trust in their expertise
        - A friendly, professional closing with next steps or encouragement

        At the end of the email, include the following sentence:
        "Please schedule a short alignment interview using the following link: {scheduling_link}"

        At the very end of the email, sign off with:
        Best regards,
        Theo Wong – Senior Manager

        Please write the entire email in plain text only. Do not use Markdown or any special formatting (e.g., asterisks, bold, or italics). Do not add any details not included above.
        """
    return prompt


def generate_email(prompt: str) -> Tuple[str, str]:
    response = client.responses.create(
        model="gpt-4o",
        instructions="You are a professional business assistant. Write concise, polite, and clear emails for business communication.",
        input=prompt,
    )

    content = response.output_text
    subject, body = content.split("\n", 1)
    # print(content)
    # print(subject)
    # print(body)
    return subject, body


def send_email(receiver: str, subject: str, body: str):
    # Build the email
    msg = MIMEMultipart()
    msg['From'] = 'hackathon.hyw.2025@gmail.com'
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send it via Gmail SMTP
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('hackathon.hyw.2025@gmail.com', 'xfpxvloxywksskhh')
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
