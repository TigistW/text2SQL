from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.vector_stores.weaviate import WeaviateVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from pinecone import Pinecone
import weaviate
from dotenv import load_dotenv
import os

def query_database(
    query: str,
    vector_store: str,
    embed_model: str,
    embed_batch_size: int = 10,
    index_name: str = None,
    top_k: int = 5,
):

    load_dotenv()

    if vector_store not in ["pinecone", "weaviate"]:
        raise ValueError(
            f"{vector_store} is not supported. Currently supported: 'pinecone' or 'weaviate'"
        )

    if vector_store == "pinecone":
        pinecone_api_key = os.environ.get("PINECONE_API_KEY")
        if pinecone_api_key is None:
            raise ValueError(
                "PINECONE_API_KEY must be specified as an environment variable."
            )
        if index_name is None:
            index_name = "schema-index"

        pc = Pinecone(api_key=pinecone_api_key)
        pc_index = pc.Index(name=index_name)
        vector_store = PineconeVectorStore(
            pinecone_index=pc_index, api_key=pinecone_api_key
        )

    elif vector_store == "weaviate":

        if index_name is None:
            index_name = "SchemaIndex"

        WEAVIATE_HOST = os.environ.get("WEAVIATE_HOST")
        client = weaviate.Client(url=WEAVIATE_HOST)
        vector_store = WeaviateVectorStore(
            weaviate_client=client, index_name=index_name
        )

    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY must be specified as an environment variable.")

    retriever = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=OpenAIEmbedding(
            model=embed_model, embed_batch_size=embed_batch_size, api_key=openai_api_key
        ),
    ).as_retriever(similarity_top_k=top_k)

    nodes = retriever.retrieve(query)

    return nodes


if __name__ == "__main__":
    from utils import setup_logger

    logger = setup_logger(__name__)
    query = "How does the prevalence of specific conditions vary across different age groups and ethnicities within our patient population?"

    try:
        nodes = query_database(query, "weaviate", "text-embedding-3-small")
    except Exception as e:
        logger.error(f"Failed to query vector database: {e}")

    for node in nodes:
        title = node.metadata["title"]
        print(f"Table: {title}")
        print(f"Similarity Score: {node.get_score()}")
        print(f"Schems: {node.get_text()}")
