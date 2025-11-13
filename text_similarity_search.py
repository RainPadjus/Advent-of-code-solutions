"""
Simple and Effective Text Similarity Search using Embeddings
Chunks documents and performs similarity search against queries.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict
import re


class TextSimilaritySearch:
    """
    A simple class for chunking documents and performing similarity search.
    """

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize with a sentence transformer model.

        Args:
            model_name: Name of the sentence-transformers model to use.
                       'all-MiniLM-L6-v2' is fast and produces 384-dim embeddings.
        """
        print(f"Loading model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.embeddings = None
        self.metadata = []
        print("Model loaded successfully!")

    def chunk_text(self, text: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
        """
        Chunk text into overlapping segments by words.

        Args:
            text: Input text to chunk
            chunk_size: Number of words per chunk
            overlap: Number of overlapping words between chunks

        Returns:
            List of text chunks
        """
        # Split by whitespace
        words = text.split()
        chunks = []

        if len(words) <= chunk_size:
            return [text]

        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:  # Avoid empty chunks
                chunks.append(chunk)

            # Stop if we've covered all words
            if i + chunk_size >= len(words):
                break

        return chunks

    def chunk_by_sentences(self, text: str, sentences_per_chunk: int = 3) -> List[str]:
        """
        Chunk text by sentences (more semantic chunking).

        Args:
            text: Input text to chunk
            sentences_per_chunk: Number of sentences per chunk

        Returns:
            List of text chunks
        """
        # Simple sentence splitting (can be improved with spacy/nltk if needed)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        for i in range(0, len(sentences), sentences_per_chunk):
            chunk = '. '.join(sentences[i:i + sentences_per_chunk])
            if chunk:
                chunks.append(chunk + '.')

        return chunks

    def add_documents(self, documents: List[str], doc_names: List[str] = None,
                     chunk_method: str = 'words', **chunk_kwargs):
        """
        Add documents to the corpus, chunk them, and generate embeddings.

        Args:
            documents: List of document texts
            doc_names: Optional list of document names/IDs
            chunk_method: 'words' or 'sentences'
            **chunk_kwargs: Additional arguments for chunking (chunk_size, overlap, etc.)
        """
        print(f"Processing {len(documents)} documents...")

        if doc_names is None:
            doc_names = [f"doc_{i}" for i in range(len(documents))]

        # Chunk all documents
        for doc_idx, (doc, doc_name) in enumerate(zip(documents, doc_names)):
            if chunk_method == 'words':
                doc_chunks = self.chunk_text(doc, **chunk_kwargs)
            elif chunk_method == 'sentences':
                doc_chunks = self.chunk_by_sentences(doc, **chunk_kwargs)
            else:
                raise ValueError(f"Unknown chunk_method: {chunk_method}")

            # Store chunks with metadata
            for chunk_idx, chunk in enumerate(doc_chunks):
                self.chunks.append(chunk)
                self.metadata.append({
                    'doc_name': doc_name,
                    'doc_idx': doc_idx,
                    'chunk_idx': chunk_idx,
                    'total_chunks': len(doc_chunks)
                })

        print(f"Created {len(self.chunks)} chunks from {len(documents)} documents")

        # Generate embeddings for all chunks
        print("Generating embeddings...")
        self.embeddings = self.model.encode(self.chunks,
                                           convert_to_numpy=True,
                                           show_progress_bar=True)
        print(f"Embeddings shape: {self.embeddings.shape}")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Search for most similar chunks to the query.

        Args:
            query: Search query text
            top_k: Number of top results to return

        Returns:
            List of dictionaries with results and metadata
        """
        if self.embeddings is None:
            raise ValueError("No documents added yet. Call add_documents() first.")

        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)[0]

        # Compute cosine similarity
        similarities = self.cosine_similarity(query_embedding, self.embeddings)

        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        # Prepare results
        results = []
        for idx in top_indices:
            results.append({
                'chunk': self.chunks[idx],
                'similarity': float(similarities[idx]),
                'metadata': self.metadata[idx]
            })

        return results

    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarity between a vector and a matrix of vectors.

        Args:
            vec1: Single vector (1D array)
            vec2: Matrix of vectors (2D array)

        Returns:
            Array of similarity scores
        """
        # Normalize vectors
        vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-8)
        vec2_norm = vec2 / (np.linalg.norm(vec2, axis=1, keepdims=True) + 1e-8)

        # Compute dot product
        return np.dot(vec2_norm, vec1_norm)

    def get_stats(self) -> Dict:
        """Get statistics about the indexed corpus."""
        return {
            'total_chunks': len(self.chunks),
            'total_documents': len(set(m['doc_name'] for m in self.metadata)),
            'embedding_dim': self.embeddings.shape[1] if self.embeddings is not None else 0,
            'model': self.model.get_sentence_embedding_dimension()
        }


def print_results(results: List[Dict], query: str):
    """Pretty print search results."""
    print(f"\n{'='*80}")
    print(f"Query: '{query}'")
    print(f"{'='*80}\n")

    for i, result in enumerate(results, 1):
        print(f"Result {i} (Similarity: {result['similarity']:.4f})")
        print(f"Document: {result['metadata']['doc_name']}")
        print(f"Chunk {result['metadata']['chunk_idx'] + 1}/{result['metadata']['total_chunks']}")
        print(f"Text: {result['chunk'][:200]}...")
        print(f"{'-'*80}\n")


if __name__ == "__main__":
    # Example usage
    print("Text Similarity Search - Example Usage\n")

    # Sample documents
    sample_docs = [
        "Python is a high-level programming language. It emphasizes code readability and simplicity.",
        "Machine learning is a subset of artificial intelligence that focuses on data-driven predictions.",
        "Climate change affects global weather patterns and requires immediate action."
    ]

    # Initialize search system
    search = TextSimilaritySearch()

    # Add documents
    search.add_documents(
        sample_docs,
        doc_names=['python_doc', 'ml_doc', 'climate_doc'],
        chunk_method='sentences',
        sentences_per_chunk=1
    )

    # Print stats
    print("\nCorpus Statistics:", search.get_stats())

    # Perform search
    query = "programming languages"
    results = search.search(query, top_k=3)
    print_results(results, query)
