import openai

class DescriptionScoringAgent:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def description_scoring_func(self, project_description: str, candidate_descritpion: str) -> str:
        prompt = (
            f"""Project Requirement: {project_description}\n
            Candidate Profile: {candidate_descritpion}\n
            Based on the above, explain why this candidate could be a good match for the project. Keep the explaination short and crisp."
            
            Instruction: 
            1. Critically asses the candidates description with that of the project description
            2. Format your response as follows:\n\n
            Explanation: [Explanation in one sentence for the score]\n"
            Description_Score: [Score (0-10)]"""
        )

        # Call to OpenAI GPT model
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crtical analyzer that provides recruitment insights based on the project requirement and the candidates profile."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250,
            
        )

        description_explanation = response.choices[0].message.content.split("Description_Score: ")[0].split("Explanation: ")[1]
        description_score = response.choices[0].message.content.split("Description_Score: ")[1]

        return description_score, description_explanation