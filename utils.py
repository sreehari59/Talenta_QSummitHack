import time
from explainable_agent import ExplanationAgent
from geo_lang_scorer import GeoLangScoringAgent
from description_scorer import DescriptionScoringAgent
from seniority_scorer import SeniorityScoringAgent
from skills_scorer import SkillScoringAgent

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

            # profile_details = f"""Role: {role}-Technologies: {technologies}-Candidate description: {profile_description}"""
            # explanation, score = explainable_ai_agent.explain_match(project_details, profile_details, similarity_score)

            description_score, description_explanation = desc_scorer.description_scoring_func(project_description, profile_description)

            # Seniority Scorer
            seniority_score, seniority_explanation = seniority_scorer.seniority_scoring_func(recommended_seniority, seniority)

            # Location Language Scorer
            geo_lang_score, geo_lang_explanation = geo_lang_scorer.geo_lang_scoring_func(location, languages_spoken)

            # Skill Scorer
            skill_score, skills_explanation = skill_scorer.skills_scoring_func(skill_required, technologies,
                                                       certificates)

            # print("********************")
            # print("description_score", description_score)
            # print("seniority_score", seniority_score)
            # print("geo_lang_score", geo_lang_score)
            # print("skill_score", skill_score)
            # print("similarity_score", similarity_score)
            # print("********************")
            # print("description_explanation", description_explanation)
            # print("seniority_explanation", seniority_explanation)
            # print("geo_lang_explanation", geo_lang_explanation)
            # print("skills_explanation", skills_explanation)
            # print("********************")

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