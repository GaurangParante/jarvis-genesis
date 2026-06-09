import json
import faiss
import numpy as np

from app.embeddings.embedding_service import EmbeddingService


class SemanticRouter:

    def __init__(self):

        self.embedding_service = (
            EmbeddingService()
        )

        self.index = faiss.read_index(
            "app/vectorstore/faiss_index.bin"
        )

        with open(
            "app/vectorstore/metadata.json",
            "r",
            encoding="utf-8"
        ) as f:

            self.metadata = json.load(f)

    def detect_agent(
        self,
        user_input,
        threshold=0.25
    ):

        vector = (
            self.embedding_service.encode(
                user_input
            )
        )

        vector = np.array(
            [vector],
            dtype="float32"
        )

        scores, indices = self.index.search(
            vector,
            3
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            results.append(
                {
                    "agent": self.metadata[idx]["name"],
                    "score": float(score)
                }
            )

        best = results[0]

        if best["score"] >= threshold:

            return {
                "matched": True,
                "agent": best["agent"],
                "score": best["score"],
                "results": results
            }
        
        print("\n[SEMANTIC ROUTER]")

        for result in results:

            print(
                f"{result['agent']} "
                f"-> {result['score']:.3f}"
            )

        return {
            "matched": False,
            "results": results
        }