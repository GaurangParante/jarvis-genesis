import json
import faiss
import numpy as np

from app.core.agent_registry import AgentRegistry
from app.embeddings.embedding_service import EmbeddingService


class VectorIndexBuilder:

    def __init__(self):

        self.registry = AgentRegistry()
        self.embedding_service = EmbeddingService()

    def build(self):

        documents = self.registry.get_agent_documents()

        embeddings = []
        metadata = []

        for doc in documents:

            vector = self.embedding_service.encode(
                doc["text"]
            )

            embeddings.append(vector)

            metadata.append(
                {
                    "name": doc["name"],
                    "text": doc["text"]
                }
            )

        embeddings = np.array(
            embeddings,
            dtype="float32"
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(embeddings)

        faiss.write_index(
            index,
            "app/vectorstore/faiss_index.bin"
        )

        with open(
            "app/vectorstore/metadata.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                metadata,
                f,
                indent=4
            )

        print(
            f"Indexed {len(metadata)} agents."
        )


if __name__ == "__main__":

    VectorIndexBuilder().build()