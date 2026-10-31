from langchain_experimental.graph_transformers import LLMGraphTransformer
docs = LLMGraphTransformer().transform_documents(raw_docs)
Neo4jGraph.from_documents(docs)          # writes nodes + relations

# hybrid: vector index on Document nodes
#         traversal on Person / Project nodes
