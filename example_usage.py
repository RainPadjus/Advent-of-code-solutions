"""
Example usage of the Text Similarity Search system with sample articles.
"""

import os
from pathlib import Path
from text_similarity_search import TextSimilaritySearch, print_results


def load_articles_from_directory(directory: str) -> tuple:
    """
    Load all text files from a directory.

    Args:
        directory: Path to directory containing text files

    Returns:
        Tuple of (documents, document_names)
    """
    directory_path = Path(directory)
    documents = []
    doc_names = []

    for file_path in sorted(directory_path.glob('*.txt')):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            doc_names.append(file_path.stem)

    return documents, doc_names


def main():
    """Main example demonstrating the text similarity search."""

    print("="*80)
    print("Text Similarity Search - Complete Example")
    print("="*80)
    print()

    # Load articles from sample_articles directory
    articles_dir = "sample_articles"

    if not os.path.exists(articles_dir):
        print(f"Error: {articles_dir} directory not found!")
        print("Please make sure the sample_articles directory exists.")
        return

    print(f"Loading articles from '{articles_dir}' directory...")
    documents, doc_names = load_articles_from_directory(articles_dir)
    print(f"Loaded {len(documents)} articles: {', '.join(doc_names)}")
    print()

    # Initialize the search system
    # Using 'all-MiniLM-L6-v2' - fast and efficient (384-dim embeddings)
    # Alternative models:
    #   - 'all-mpnet-base-v2': Higher quality but slower (768-dim)
    #   - 'paraphrase-multilingual-MiniLM-L12-v2': For multilingual support
    search = TextSimilaritySearch(model_name='all-MiniLM-L6-v2')

    # Add documents with sentence-based chunking
    print("Processing documents and generating embeddings...")
    search.add_documents(
        documents,
        doc_names=doc_names,
        chunk_method='sentences',
        sentences_per_chunk=3  # Group 3 sentences per chunk
    )
    print()

    # Display corpus statistics
    stats = search.get_stats()
    print("Corpus Statistics:")
    print(f"  - Total documents: {stats['total_documents']}")
    print(f"  - Total chunks: {stats['total_chunks']}")
    print(f"  - Embedding dimensions: {stats['embedding_dim']}")
    print()

    # Example queries
    queries = [
        "How do neural networks work?",
        "What programming languages are good for beginners?",
        "Tell me about renewable energy and environmental issues",
        "What are the applications of quantum physics in computing?",
        "How does cryptocurrency technology work?"
    ]

    # Perform searches
    for query in queries:
        results = search.search(query, top_k=3)
        print_results(results, query)
        input("Press Enter to see next query results...\n")

    # Interactive search
    print("\n" + "="*80)
    print("Interactive Search Mode")
    print("="*80)
    print("Enter your queries (or 'quit' to exit):\n")

    while True:
        query = input("Query: ").strip()

        if query.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break

        if not query:
            continue

        results = search.search(query, top_k=5)
        print_results(results, query)


if __name__ == "__main__":
    main()
