import openai

class GeoLangScoringAgent:
    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key

    def geo_lang_scoring_func(self, project_location: str, candidate_lang_skill: str) -> str:

        prompt = (
            f"""Project Location: {project_location}\n
            Candidate Language Skills: {candidate_lang_skill}\n
            Consider the job location and what language does the country speak. Look into the  Candidate Language Skills
            and see if the candidate can speak the official langugae of the place. If the candidate can speak give a score of 5. If the 
            candidate cannot speak then give a score of 0. 
            
            Example:

            User Input:
            Project Location: Munich
            Candidate Language Skills: German, English
            
            Assistant Thinking
            The project location is Munich. Munich is a place in Germany. Official language of Germany is German.
            From the candidate language skill, the candidate can speak German. 

            Assistant:
            Score: 10

            Instruction: 
            1. Critically analyze the Project Location and Candidate Language Skills and finally give a score.
            2. Format your response as follows:\n\n
            Explanation: [One sentence why the score.]\n
            Language_Score: [Score (0-5)]"""
        )

        # Call to OpenAI GPT model
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a crtical analyzer that provides recruitment insights based on the project requirement and the candidates profile."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=250,
            
        )

        geo_lang_explanation = response.choices[0].message.content.split("Language_Score: ")[0].split("Explanation: ")[1]
        geo_lang_score = response.choices[0].message.content.split("Language_Score: ")[1]

        return geo_lang_score, geo_lang_explanation