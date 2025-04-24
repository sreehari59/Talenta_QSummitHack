import openai

class SkillScoringAgent:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def skills_scoring_func(self, project_skills_requirement: str, candidate_skills: str, candidate_certification: str) -> str:
        prompt = (
            f"""Project Skills Requirement: {project_skills_requirement}\n
            Candidate Skills: {candidate_skills}\n
            Candidate Certification: {candidate_certification}\n
            What are the 5 skills that the candidate gained from completion of the certification and keep in mind.
            
            Instruction: 
            1. Critically assess strictly the required Project skills with  the candidate technology skills  + 
            the 5 skills that the candidate gained from completion of the certification and keep in mind. Score it out of 15. Candidate that matches all the required project skills to be given a score of 12 or above.
            2. Format your response as follows:\n\n
            Explanation: [list two sentences with the matched skills and missing skills.]\n"
            Skills_Score: [Score (0-15)]"""
        )

        # Call to OpenAI GPT model
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crtical analyzer that assesses whether the candidates skills match the project skills requirement."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250,
            
        )

        skills_explanation = response.choices[0].message.content.split("Skills_Score:")[0].split("Explanation: ")[1].strip()
        skills_score = response.choices[0].message.content.split("Skills_Score: ")[1]

        return skills_score, skills_explanation