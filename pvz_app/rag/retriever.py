from langchain_community.embeddings import HuggingFaceEmbeddings

def retriever_init():
    retriever = HuggingFaceEmbeddings(
        model_name='C:/Users/nik_p/Desktop/wb_proj/wb_project/models/finetuned_sergeyzh_rubert_tiny_turbo'
    )
    return retriever
