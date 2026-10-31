# Construction
from langchain_experimental.graph_transformers import LLMGraphTransformer
transformer = LLMGraphTransformer(llm=ChatOpenAI(model="gpt-4o"))
graph_docs = await transformer.convert_to_graph_documents(raw_docs)

# Storage
from langchain_community.graphs import Neo4jGraph
graph = Neo4jGraph(url="bolt://localhost:7687", username="neo4j", password="***")
graph.add_graph_documents(graph_docs)

# Retrieval
from langchain_community.chains import GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(llm=ChatOpenAI(model="gpt-4o"), graph=graph)
answer = chain.invoke("Who approved project X?")
