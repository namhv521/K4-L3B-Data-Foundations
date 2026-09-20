from __future__ import annotations
import copy
from typing import Any, Callable
from .chunking import _dot
from .embeddings import _mock_embed
from .models import Document

class EmbeddingStore:
    def __init__(self, collection_name: str = "documents", embedding_fn: Callable[[str], list[float]] | None = None) -> None:
        self._embedding_fn = embedding_fn or _mock_embed
        self._collection_name = collection_name
        self._use_chroma = False
        self._store: list[dict[str, Any]] = []
        self._collection = None
        self._next_index = 0

    def _make_record(self, doc: Document) -> dict[str, Any]:
        embedding = self._embedding_fn(doc.content)
        meta = copy.deepcopy(doc.metadata) if doc.metadata else {}
        if "doc_id" not in meta:
            meta["doc_id"] = doc.id
        return {
            "id": doc.id,
            "content": doc.content,
            "metadata": meta,
            "embedding": embedding,
        }

    def _search_records(self, query: str, records: list[dict[str, Any]], top_k: int) -> list[dict[str, Any]]:
        if not records or top_k <= 0:
            return []
        query_vec = self._embedding_fn(query)
        scored: list[tuple[float, dict[str, Any]]] = []
        for rec in records:
            score = _dot(query_vec, rec["embedding"])
            scored.append((score, rec))

        scored.sort(key=lambda x: x[0], reverse=True)
        results: list[dict[str, Any]] = []
        for score, rec in scored[:top_k]:
            results.append({
                "id": rec["id"],
                "content": rec["content"],
                "metadata": rec["metadata"],
                "score": score,
            })
        return results

    def add_documents(self, docs: list[Document]) -> None:
        for doc in docs:
            record = self._make_record(doc)
            self._store.append(record)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        return self._search_records(query, self._store, top_k=top_k)

    def get_collection_size(self) -> int:
        return len(self._store)

    def search_with_filter(self, query: str, top_k: int = 3, metadata_filter: dict = None) -> list[dict]:
        if not metadata_filter:
            return self.search(query, top_k=top_k)
        filtered_records = []
        for rec in self._store:
            rec_meta = rec.get("metadata", {})
            match = True
            for k, v in metadata_filter.items():
                if rec_meta.get(k) != v:
                    match = False
                    break
            if match:
                filtered_records.append(rec)
        return self._search_records(query, filtered_records, top_k=top_k)

    def delete_document(self, doc_id: str) -> bool:
        initial_len = len(self._store)
        self._store = [
            rec for rec in self._store
            if rec.get("metadata", {}).get("doc_id") != doc_id and rec.get("id") != doc_id
        ]
        return len(self._store) < initial_len