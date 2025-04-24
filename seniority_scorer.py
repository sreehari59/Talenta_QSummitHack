import openai

class SeniorityScoringAgent:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def seniority_scoring_func(self, project_recommended_seniority: str, candidate_seniority: str) -> str:
        prompt = (
            f"""Project recommended seniority Requirement: {project_recommended_seniority}\n
            candidate seniority: {candidate_seniority}\n
            
            Instruction: 
            1. assess the required Project seniority with the candidates seniority.
            2. Format your response as follows:\n\n
            Explanation: [Is seniority satisfied? Explain in One sentence.]\n"
            Seniority_Score: [Score (0-5)]"""
        )

        # Call to OpenAI GPT model
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crtical analyzer that assesses whether the candidates seniority matches the project recommended seniority."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=250,
            
        )

        seniority_explanation = response.choices[0].message.content.split("Seniority_Score: ")[0].strip()
        seniority_score = response.choices[0].message.content.split("Seniority_Score: ")[1]

        return seniority_score, seniority_explanation