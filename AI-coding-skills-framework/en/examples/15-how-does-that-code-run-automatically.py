from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Load the existing vector DB
vector_store = Chroma(
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    persist_directory="./chroma_db"
)

# Create the chain: automatic retrieve + augment + generate
qa_chain = RetrievalQA.from_chain_type(
    llm=Ollama(model="gemma3:12b"),
    retriever=vector_store.as_retriever(),
    chain_type="stuff"  # stuff = stuffs the context into the prompt
)

# Use it: automatically runs retrieve → augment → LLM
result = qa_chain.invoke("Does health insurance cover heart disease?")
print(result)
