from langchain_community.embeddings import HuggingFaceEmbeddings

def retriever_init():
    retriever = HuggingFaceEmbeddings(
        model_name='C:/Users/nik_p/Desktop/wb_proj/wb_project/models/fine_tuned_model'
    )
    return retriever
