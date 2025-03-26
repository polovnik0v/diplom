import pandas as pd
from langchain_community.vectorstores import FAISS
from .retriever import retriever_init

retriever = retriever_init()

chunks = pd.read_csv('C:/Users/nik_p/Desktop/diplom/pvz_helper/data/chunks.csv')
texts = chunks['Chunk'].tolist()
faiss_index = FAISS.from_texts(texts, retriever)

def find_relevant_chunks(question, top_n=5):
    # Поиск релевантных чанков с использованием FAISS
    results = faiss_index.similarity_search(question, k=top_n)
    return results
