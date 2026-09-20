from typing import Callable
from .store import EmbeddingStore

class KnowledgeBaseAgent:
    def __init__(self, store: EmbeddingStore, llm_fn: Callable[[str], str]) -> None:
        self.store = store
        self.llm_fn = llm_fn

    def answer(self, question: str, top_k: int = 3) -> str:
        results = self.store.search(question, top_k=top_k)
        if not results:
            return "Xin lỗi, tôi không tìm thấy thông tin liên quan trong cơ sở tri thức để trả lời câu hỏi này."

        context_blocks = []
        for i, res in enumerate(results, start=1):
            source = res.get("metadata", {}).get("doc_id", res.get("id", "unknown"))
            context_blocks.append(f"[{i}] (Nguồn: {source}):\\n{res['content']}")

        context_str = "\\n\\n".join(context_blocks)
        prompt = (
            f"Bạn là trợ lý AI hỗ trợ giải đáp chính sách thương mại điện tử dựa trên tài liệu được cung cấp.\\n"
            f"Hãy trả lời câu hỏi dưới đây CHỈ dựa trên ngữ cảnh được cung cấp. Nếu ngữ cảnh không có thông tin, hãy nêu rõ là không tìm thấy, không tự suy đoán.\\n"
            f"Khi trả lời, hãy trích dẫn số thứ tự nguồn [1], [2] tương ứng.\\n\\n"
            f"--- NGỮ CẢNH ---\\n{context_str}\\n\\n"
            f"--- CÂU HỎI ---\\n{question}\\n\\n"
            f"--- CÂU TRẢ LỜI ---"
        )
        return self.llm_fn(prompt)