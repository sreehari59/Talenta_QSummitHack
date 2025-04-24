import openai

class ExplanationAgent:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def explain_match(self, project_requirement: str, candidate_profile: str, cosine_similarity: str) -> str:
        """
        Generates an explanation for why a candidate might be a match for a project
        and returns a match score as a percentage.

        Args:
            project_requirement (str): Description of the project requirements.
            candidate_profile (str): Description of the candidate's skills and experience.
            cosine_similarity (str): Cosine similarity score between 0 and 1.

        """
        prompt = (
            f"""Project Requirement: {project_requirement}\n
            Candidate Profile: {candidate_profile}\n
            Based on the above, explain why this candidate could be a good match for the project. Keep the explaination short and crisp."
            
            Instruction: 
            1. Critically asses the user's skills with that of the project skills and description
            2. Format your response as follows:\n\n
            Explanation: [Explanation of the match]\n"
            Score: [Score (0-100)]"""
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

        explanation = response.choices[0].message.content.split("Score:")[0].strip()
        score = response.choices[0].message.content.split("Score: ")[1]

        return explanation, score