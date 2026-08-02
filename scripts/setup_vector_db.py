import os
import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'chromadb')

def setup_db():
    print("Initializing embeddings model...")
    # Use a small, fast sentence transformer model for local CPU testing
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Creating mock clinical guidelines with species metadata...")
    documents = [
        Document(
            page_content="Early administration of broad-spectrum antibiotics within 1 hour of recognition is recommended for adult patients with sepsis.",
            metadata={"species": "human"}
        ),
        Document(
            page_content="For adult human patients with high-risk neutropenic fever, consider adding antifungal coverage if fever persists after 4-7 days.",
            metadata={"species": "human"}
        ),
        Document(
            page_content="If VIM, IMP, or NDM metallo-beta-lactamase genes are detected in a human isolate, consider Cefiderocol or aztreonam-avibactam.",
            metadata={"species": "human"}
        ),
        Document(
            page_content="In canine septic peritonitis, immediate surgical source control and IV enrofloxacin + ampicillin/sulbactam is recommended.",
            metadata={"species": "canine"}
        ),
        Document(
            page_content="Canine isolates showing resistance to cephalexin (e.g. methicillin-resistant S. pseudintermedius) should be treated with clindamycin or doxycycline if susceptible.",
            metadata={"species": "canine"}
        ),
        Document(
            page_content="Bovine mastitis caused by Staphylococcus aureus may be refractory to beta-lactams; cull chronic offenders or use targeted intramammary ceftiofur.",
            metadata={"species": "bovine"}
        ),
        Document(
            page_content="Bovine respiratory disease (BRD) complex with suspected Mycoplasma bovis resistance requires tulathromycin or florfenicol, avoiding penicillins.",
            metadata={"species": "bovine"}
        )
    ]
    
    print(f"Creating Chroma vector store at {DB_DIR}...")
    os.makedirs(DB_DIR, exist_ok=True)
    
    vectorstore = Chroma.from_documents(
        documents=documents, 
        embedding=embeddings, 
        persist_directory=DB_DIR
    )
    vectorstore.persist()
    print("Vector store successfully built and persisted!")

if __name__ == "__main__":
    setup_db()
