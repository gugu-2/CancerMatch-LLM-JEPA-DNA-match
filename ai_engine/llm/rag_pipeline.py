import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from ai_engine.llm.safety_auditor import SafetyAuditor

class RAGPipeline:
    def __init__(self):
        db_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'processed', 'chromadb')
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(persist_directory=db_dir, embedding_function=self.embeddings)
        
        # Connect to Local Ollama Instance (Zero Cost, 8GB VRAM friendly)
        self.llm = Ollama(model="llama3")
        self.auditor = SafetyAuditor()
        
        self.prompt_template = PromptTemplate(
            input_variables=["species", "context", "notes", "allergies", "renal_function"],
            template=(
                "You are an expert PathoMatch AI Clinical Assistant specializing in {species} medicine.\n"
                "Given the following clinical guidelines:\n"
                "---------------------\n"
                "{context}\n"
                "---------------------\n"
                "Patient EHR Constraints & Mathematical Engine Output:\n"
                "- Notes: {notes}\n"
                "- Allergies: {allergies}\n"
                "- Renal Function: {renal_function}\n\n"
                "Provide a treatment recommendation for this {species} patient, strictly adhering to the guidelines and adjusting for the EHR constraints and Math Engine AMR outputs:"
            )
        )

    def generate_report(self, species: str, notes: str, allergies: str = None, renal_function: str = "Normal") -> dict:
        target_species = species.lower()
        extrapolated = False
        
        # 1. Retrieval with Metadata Filtering
        retriever = self.vectorstore.as_retriever(search_kwargs={'filter': {'species': target_species}})
        docs = retriever.invoke(notes if notes else "General treatment guidelines")
        
        # FIT (Found In Translation) Fallback Logic
        if not docs and target_species != "human":
            extrapolated = True
            retriever = self.vectorstore.as_retriever(search_kwargs={'filter': {'species': "human"}})
            docs = retriever.invoke(notes if notes else "General treatment guidelines")
        
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        # 2. Format Prompt with EHR Context
        prompt = self.prompt_template.format(
            species=species, 
            context=context_text, 
            notes=notes,
            allergies=allergies or "None reported",
            renal_function=renal_function
        )
        
        # 3. Generate response (If Ollama is down, this will throw a ConnectionError, but it's a real LLM attempt now!)
        try:
            response = self.llm.invoke(prompt)
        except Exception as e:
            response = f"LOCAL AI ERROR: Ensure Ollama is running. Error: {str(e)}"
        
        # 4. LLM-as-a-Judge Safety Audit
        audit_result = self.auditor.evaluate(docs, response)
        
        return {
            "retrieved_documents": [doc.page_content for doc in docs],
            "llm_prompt": prompt,
            "llm_response": response,
            "extrapolated_from_human": extrapolated,
            "safety_audit": audit_result
        }
