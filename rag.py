from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.schema import Document
from qdrant_client import models
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate

class RagModel():
    def __init__(self, api_keys, qdrant_api_key, qdrant_url, qdrant_collection_name,
                embedding_model="text-embedding-3-large", model="gpt-4o-mini", number_of_profiles_required = 2):
        self.apikeys = api_keys
        self.qdrant_api_key = qdrant_api_key
        self.qdrant_url = qdrant_url
        self.qdrant_collection_name = qdrant_collection_name
        self.model = model
        self.number_of_profiles_required = number_of_profiles_required
        self.embedding = OpenAIEmbeddings( api_key = api_keys, model= embedding_model)

    def retrieve_data(self, user_input, number_of_doc, resolved_ticket_flag):
        
        qdrant = QdrantVectorStore.from_existing_collection(
                            embedding = self.embedding,
                            collection_name = self.qdrant_collection_name,
                            url = self.qdrant_url,
                            api_key = self.qdrant_api_key,
                        )
        
        if resolved_ticket_flag:
            filters = models.Filter(must=[models.FieldCondition(
                                key="metadata.absolute",
                                match=models.MatchValue(value=True),
                            ),])
            qdrant_retriever = qdrant.as_retriever(search_type="similarity", search_kwargs={"k": number_of_doc + self.number_of_profiles_required, "filter": filters})
        else:
            qdrant_retriever = qdrant.as_retriever(search_type="similarity", search_kwargs={"k": number_of_doc + self.number_of_profiles_required})

        sim_response = qdrant.similarity_search_with_score(user_input,  number_of_doc + 2)

        return sim_response
    
    def upload_data(self, data):
        docs = []
        for _, row in data.iterrows():
            content = f"""role: {row['role']}-technologies: {', '.join(row['technologies'])}-seniority: {row['seniority']}-
            description: {row['description']}-certificates: {', '.join(row['certificates'])}- 
            languages_spoken: {', '.join(row['languages_spoken'])}"""
      
            doc = Document(page_content=content,
                           metadata={
                               "name": row["name"],
                               "role": row["role"],
                               "description": row["description"],
                               "seniority": row["seniority"],
                               "languages_spoken":', '.join(row['languages_spoken']),
                               "certificates":', '.join(row['certificates']),
                               "technologies":', '.join(row['technologies']),
                                    }
                                )
            docs.append(doc)
        print("embedding_model:",self.embedding)
        qdrant = QdrantVectorStore.from_documents(
                    docs,
                    embedding = self.embedding,
                    url = self.qdrant_url,
                    prefer_grpc=True,
                    api_key = self.qdrant_api_key,
                    collection_name = self.qdrant_collection_name,
                )
        
        return self.qdrant_collection_name

    
