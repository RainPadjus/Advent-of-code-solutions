# Text Similarity Search with Embeddings

A simple, fast, and effective Python implementation for semantic text search using sentence embeddings. Perfect for searching through article collections, documentation, or any text corpus.

## Features

- **Fast embedding generation** using sentence-transformers
- **Flexible chunking strategies** (word-based or sentence-based)
- **Cosine similarity search** for finding relevant text passages
- **Metadata tracking** for each chunk (source document, position, etc.)
- **Easy-to-use API** with minimal setup

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

This will install:
- `sentence-transformers` - For generating text embeddings
- `numpy` - For efficient similarity calculations
- `torch` - Backend for the transformer models

### Basic Usage

```python
from text_similarity_search import TextSimilaritySearch

# Initialize the search system
search = TextSimilaritySearch()

# Add your documents
documents = [
    "Python is a versatile programming language...",
    "Machine learning enables computers to learn from data...",
    "Climate change is a pressing global issue..."
]

search.add_documents(
    documents,
    doc_names=['doc1', 'doc2', 'doc3'],
    chunk_method='sentences',
    sentences_per_chunk=3
)

# Search!
results = search.search("programming languages", top_k=5)

# Print results
for result in results:
    print(f"Similarity: {result['similarity']:.4f}")
    print(f"Text: {result['chunk']}")
    print(f"Source: {result['metadata']['doc_name']}")
```

### Run the Example

Try the included example with sample articles:

```bash
python example_usage.py
```

This will:
1. Load 5 sample articles on various topics
2. Chunk and embed all documents
3. Run example queries
4. Enter interactive search mode

## How It Works

### 1. Chunking

The system breaks documents into smaller, overlapping chunks:

**Word-based chunking:**
```python
search.add_documents(
    documents,
    chunk_method='words',
    chunk_size=200,    # 200 words per chunk
    overlap=50         # 50 word overlap between chunks
)
```

**Sentence-based chunking (recommended):**
```python
search.add_documents(
    documents,
    chunk_method='sentences',
    sentences_per_chunk=3  # 3 sentences per chunk
)
```

### 2. Embedding Generation

Uses sentence-transformers to convert text chunks into dense vector representations:

- **Default model:** `all-MiniLM-L6-v2`
  - Fast and efficient
  - 384-dimensional embeddings
  - Good balance of speed and quality

- **Alternative models:**
  - `all-mpnet-base-v2` - Higher quality (768-dim), slower
  - `paraphrase-multilingual-MiniLM-L12-v2` - Multilingual support

### 3. Similarity Search

Computes cosine similarity between query embedding and all chunk embeddings:

```python
results = search.search("your query", top_k=5)
```

Returns the top-k most similar chunks with metadata.

## API Reference

### TextSimilaritySearch

#### `__init__(model_name: str = 'all-MiniLM-L6-v2')`

Initialize the search system with a sentence-transformer model.

#### `add_documents(documents, doc_names=None, chunk_method='words', **chunk_kwargs)`

Add documents to the searchable corpus.

**Parameters:**
- `documents`: List of document texts
- `doc_names`: Optional list of document identifiers
- `chunk_method`: `'words'` or `'sentences'`
- `**chunk_kwargs`: Chunking parameters
  - For words: `chunk_size`, `overlap`
  - For sentences: `sentences_per_chunk`

#### `search(query: str, top_k: int = 5)`

Search for most similar chunks.

**Returns:** List of dictionaries with:
- `chunk`: The text chunk
- `similarity`: Cosine similarity score (0-1)
- `metadata`: Dictionary with document info

#### `get_stats()`

Get corpus statistics.

**Returns:** Dictionary with:
- `total_chunks`: Number of chunks
- `total_documents`: Number of documents
- `embedding_dim`: Embedding dimensionality

## Example Use Cases

### 1. Document Search

```python
# Load your documents
docs = load_documents_from_folder("my_docs/")
search.add_documents(docs)

# Find relevant passages
results = search.search("how to handle errors in async code", top_k=10)
```

### 2. FAQ Matching

```python
faqs = [
    "How do I reset my password? Go to settings...",
    "What payment methods are accepted? We accept...",
    # ... more FAQs
]

search.add_documents(faqs, chunk_method='sentences', sentences_per_chunk=1)
results = search.search(user_question, top_k=3)
```

### 3. Research Paper Search

```python
papers = load_papers("research_papers/")
search.add_documents(
    papers,
    chunk_method='sentences',
    sentences_per_chunk=5  # Larger chunks for academic text
)

results = search.search("attention mechanism transformers", top_k=10)
```

## Performance Tips

1. **Choose the right model:**
   - For speed: `all-MiniLM-L6-v2` (default)
   - For quality: `all-mpnet-base-v2`
   - For multilingual: `paraphrase-multilingual-MiniLM-L12-v2`

2. **Optimize chunk size:**
   - Smaller chunks: More precise but may lose context
   - Larger chunks: More context but less precise
   - Recommended: 2-5 sentences per chunk

3. **Use batch processing:**
   - The system automatically batches embedding generation
   - Process all documents at once for best performance

4. **GPU acceleration:**
   - Automatically uses GPU if available
   - Significantly faster for large corpora

## Sample Articles

The `sample_articles/` directory contains 5 example articles on:
- Python programming
- AI and Machine Learning
- Climate Change
- Quantum Computing
- Blockchain Technology

Perfect for testing and demonstrations!

## Extending the System

### Add Custom Chunking

```python
class MyCustomSearch(TextSimilaritySearch):
    def custom_chunk_method(self, text: str) -> List[str]:
        # Your custom chunking logic
        return chunks
```

### Use Different Similarity Metrics

```python
# Modify the search method to use dot product instead
def search_dotproduct(self, query, top_k=5):
    query_embedding = self.model.encode([query])[0]
    scores = np.dot(self.embeddings, query_embedding)
    # ... rest of the logic
```

## Requirements

- Python 3.7+
- sentence-transformers >= 2.2.0
- numpy >= 1.21.0
- torch >= 2.0.0

## License

Free to use for experiments and learning!

## Tips for Best Results

1. **Preprocess your text** - Remove excessive whitespace, fix encoding issues
2. **Choose appropriate chunk sizes** - Match your typical query length
3. **Use domain-specific models** if available (e.g., bio-medical, legal)
4. **Experiment with overlap** - More overlap = better context but more chunks
5. **Monitor similarity scores** - Scores above 0.5 are usually relevant

## Common Issues

**Q: Embeddings are slow to generate?**
- Use a smaller model or enable GPU acceleration

**Q: Search results aren't relevant?**
- Try different chunking strategies
- Experiment with chunk sizes
- Consider a different embedding model

**Q: Out of memory errors?**
- Process documents in batches
- Use a smaller embedding model
- Reduce chunk overlap

## Next Steps

- Add re-ranking for better results
- Implement approximate nearest neighbors (FAISS, Annoy) for large corpora
- Add filtering by metadata
- Create a REST API wrapper
- Build a web interface

Happy searching! 🔍
