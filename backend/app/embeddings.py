from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(comments):

    embeddings = model.encode(comments)

    return embeddings