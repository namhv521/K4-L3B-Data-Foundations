from __future__ import annotations
import math
import re

class FixedSizeChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []
        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            if start + self.chunk_size >= len(text):
                break
        return chunks

class SentenceChunker:
    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        self.max_sentences_per_chunk = max(1, max_sentences_per_chunk)

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        raw_sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        sentences = [s.strip() for s in raw_sentences if s.strip()]
        if not sentences:
            return []

        chunks: list[str] = []
        for i in range(0, len(sentences), self.max_sentences_per_chunk):
            group = sentences[i : i + self.max_sentences_per_chunk]
            chunk_str = " ".join(group).strip()
            if chunk_str:
                chunks.append(chunk_str)
        return chunks

class RecursiveChunker:
    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, separators: list[str] | None = None, chunk_size: int = 500) -> None:
        self.separators = self.DEFAULT_SEPARATORS if separators is None else list(separators)
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]
        return self._split(text, self.separators)

    def _split(self, current_text: str, remaining_separators: list[str]) -> list[str]:
        if not current_text:
            return []
        if len(current_text) <= self.chunk_size:
            return [current_text]
        if not remaining_separators:
            return [current_text[i : i + self.chunk_size] for i in range(0, len(current_text), self.chunk_size)]

        sep = remaining_separators[0]
        next_seps = remaining_separators[1:]

        if sep == "":
            return [current_text[i : i + self.chunk_size] for i in range(0, len(current_text), self.chunk_size)]

        splits = current_text.split(sep)
        if len(splits) == 1:
            return self._split(current_text, next_seps)

        merged_chunks: list[str] = []
        current_chunk = ""
        for piece in splits:
            if len(piece) > self.chunk_size:
                if current_chunk:
                    merged_chunks.append(current_chunk)
                    current_chunk = ""
                merged_chunks.extend(self._split(piece, next_seps))
            else:
                candidate = piece if not current_chunk else current_chunk + sep + piece
                if len(candidate) <= self.chunk_size:
                    current_chunk = candidate
                else:
                    if current_chunk:
                        merged_chunks.append(current_chunk)
                    current_chunk = piece
        if current_chunk:
            merged_chunks.append(current_chunk)
        return merged_chunks


class HeadingChunker:
    """Keep Markdown sections intact and repeat their heading after a split."""

    HEADING_PATTERN = re.compile(r"^(#{1,6}\s+.+)$", re.MULTILINE)

    def __init__(self, chunk_size: int = 500) -> None:
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []

        headings = list(self.HEADING_PATTERN.finditer(text))
        if not headings:
            return RecursiveChunker(chunk_size=self.chunk_size).chunk(text.strip())

        chunks: list[str] = []
        preamble = text[:headings[0].start()].strip()
        if preamble:
            chunks.extend(RecursiveChunker(chunk_size=self.chunk_size).chunk(preamble))

        for index, match in enumerate(headings):
            body_end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            heading = match.group(1).strip()
            body = text[match.end():body_end].strip()
            chunks.extend(self._chunk_section(heading, body))
        return chunks

    def _chunk_section(self, heading: str, body: str) -> list[str]:
        section = heading if not body else f"{heading}\n{body}"
        if len(section) <= self.chunk_size:
            return [section]
        if not body:
            return [heading]

        prefix = f"{heading}\n"
        body_chunk_size = max(1, self.chunk_size - len(prefix))
        body_chunks = RecursiveChunker(chunk_size=body_chunk_size).chunk(body)
        return [f"{prefix}{chunk.strip()}" for chunk in body_chunks if chunk.strip()]

def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))

def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot_prod = _dot(vec_a, vec_b)
    norm_a = math.sqrt(sum(x * x for x in vec_a))
    norm_b = math.sqrt(sum(y * y for y in vec_b))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_prod / (norm_a * norm_b)

class ChunkingStrategyComparator:
    def compare(self, text: str, chunk_size: int = 200) -> dict:
        fixed = FixedSizeChunker(chunk_size=chunk_size, overlap=20).chunk(text)
        sentences = SentenceChunker(max_sentences_per_chunk=2).chunk(text)
        recursive = RecursiveChunker(chunk_size=chunk_size).chunk(text)
        strategies = {"fixed_size": fixed, "by_sentences": sentences, "recursive": recursive}
        result = {}
        for name, chunks in strategies.items():
            count = len(chunks)
            avg_len = sum(len(c) for c in chunks) / count if count > 0 else 0.0
            result[name] = {"count": count, "avg_length": avg_len, "chunks": chunks}
        return result