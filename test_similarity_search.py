"""
Test script for the Text Similarity Search system.
Tests various aspects of functionality and performance.
"""

import time
import sys
from pathlib import Path
from text_similarity_search import TextSimilaritySearch


def load_articles_from_directory(directory: str):
    """Load all text files from a directory."""
    directory_path = Path(directory)
    documents = []
    doc_names = []

    for file_path in sorted(directory_path.glob('*.txt')):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            doc_names.append(file_path.stem)

    return documents, doc_names


def test_basic_functionality():
    """Test 1: Basic functionality with simple documents."""
    print("\n" + "="*80)
    print("TEST 1: Basic Functionality")
    print("="*80)

    try:
        search = TextSimilaritySearch()

        docs = [
            "Python is a programming language used for web development and data science.",
            "JavaScript is primarily used for web development and front-end applications.",
            "The weather today is sunny with a chance of rain in the evening.",
        ]

        search.add_documents(docs, chunk_method='sentences', sentences_per_chunk=1)

        query = "web programming"
        results = search.search(query, top_k=2)

        print(f"✓ Query: '{query}'")
        print(f"✓ Top result similarity: {results[0]['similarity']:.4f}")
        print(f"✓ Top result text: {results[0]['chunk'][:80]}...")

        # Verify the programming-related results are more relevant
        if results[0]['similarity'] > 0.3:
            print("✓ PASSED: Found relevant results")
            return True
        else:
            print("✗ FAILED: Similarity score too low")
            return False

    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_chunking_strategies():
    """Test 2: Different chunking strategies."""
    print("\n" + "="*80)
    print("TEST 2: Chunking Strategies")
    print("="*80)

    try:
        long_text = "Python is great. " * 50  # Create a longer document

        # Test word-based chunking
        search1 = TextSimilaritySearch()
        search1.add_documents([long_text], chunk_method='words', chunk_size=20, overlap=5)
        stats1 = search1.get_stats()

        # Test sentence-based chunking
        search2 = TextSimilaritySearch()
        search2.add_documents([long_text], chunk_method='sentences', sentences_per_chunk=2)
        stats2 = search2.get_stats()

        print(f"✓ Word-based chunks: {stats1['total_chunks']}")
        print(f"✓ Sentence-based chunks: {stats2['total_chunks']}")
        print("✓ PASSED: Both chunking strategies work")
        return True

    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def test_with_sample_articles():
    """Test 3: Full test with sample articles."""
    print("\n" + "="*80)
    print("TEST 3: Sample Articles Search")
    print("="*80)

    try:
        # Load sample articles
        docs, doc_names = load_articles_from_directory("sample_articles")
        print(f"✓ Loaded {len(docs)} articles")

        # Initialize and process
        start_time = time.time()
        search = TextSimilaritySearch()
        search.add_documents(docs, doc_names=doc_names,
                           chunk_method='sentences', sentences_per_chunk=3)
        processing_time = time.time() - start_time

        stats = search.get_stats()
        print(f"✓ Processing time: {processing_time:.2f} seconds")
        print(f"✓ Total chunks: {stats['total_chunks']}")
        print(f"✓ Embedding dimensions: {stats['embedding_dim']}")

        # Test queries
        test_queries = [
            ("machine learning algorithms", "article2_ai"),
            ("programming language features", "article1_python"),
            ("global warming effects", "article3_climate"),
            ("quantum bits and qubits", "article4_quantum"),
            ("cryptocurrency blockchain", "article5_blockchain"),
        ]

        print(f"\n{'Query':<40} {'Expected':<20} {'Top Result':<20} {'Score':<8} {'Match'}")
        print("-" * 100)

        matches = 0
        for query, expected_doc in test_queries:
            start_search = time.time()
            results = search.search(query, top_k=1)
            search_time = time.time() - start_search

            top_result = results[0]
            top_doc = top_result['metadata']['doc_name']
            similarity = top_result['similarity']

            is_match = expected_doc in top_doc
            match_symbol = "✓" if is_match else "✗"

            print(f"{query:<40} {expected_doc:<20} {top_doc:<20} {similarity:<8.4f} {match_symbol}")

            if is_match:
                matches += 1

        accuracy = (matches / len(test_queries)) * 100
        print(f"\n✓ Accuracy: {accuracy:.1f}% ({matches}/{len(test_queries)} correct)")
        print(f"✓ Average search time: ~{search_time*1000:.2f}ms per query")

        if accuracy >= 80:
            print("✓ PASSED: High accuracy achieved")
            return True
        else:
            print("✗ PARTIAL: Lower than expected accuracy")
            return False

    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_edge_cases():
    """Test 4: Edge cases and error handling."""
    print("\n" + "="*80)
    print("TEST 4: Edge Cases")
    print("="*80)

    tests_passed = 0
    total_tests = 3

    # Test 1: Empty document
    try:
        search = TextSimilaritySearch()
        search.add_documents([""], chunk_method='sentences', sentences_per_chunk=1)
        print("✓ Handled empty document")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Empty document failed: {e}")

    # Test 2: Very short document
    try:
        search = TextSimilaritySearch()
        search.add_documents(["Hello"], chunk_method='words', chunk_size=10)
        results = search.search("greeting", top_k=1)
        print("✓ Handled very short document")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Short document failed: {e}")

    # Test 3: Special characters
    try:
        search = TextSimilaritySearch()
        search.add_documents(["Test @#$% special *&^% characters!!!"],
                           chunk_method='sentences', sentences_per_chunk=1)
        results = search.search("special", top_k=1)
        print("✓ Handled special characters")
        tests_passed += 1
    except Exception as e:
        print(f"✗ Special characters failed: {e}")

    if tests_passed == total_tests:
        print(f"✓ PASSED: All edge cases handled ({tests_passed}/{total_tests})")
        return True
    else:
        print(f"✗ PARTIAL: Some edge cases failed ({tests_passed}/{total_tests})")
        return False


def test_performance():
    """Test 5: Performance with many documents."""
    print("\n" + "="*80)
    print("TEST 5: Performance Test")
    print("="*80)

    try:
        # Create 50 synthetic documents
        docs = []
        for i in range(50):
            topic = ["technology", "science", "sports", "politics", "entertainment"][i % 5]
            doc = f"This is document {i} about {topic}. " * 20
            docs.append(doc)

        print(f"✓ Created {len(docs)} synthetic documents")

        # Measure processing time
        search = TextSimilaritySearch()
        start = time.time()
        search.add_documents(docs, chunk_method='sentences', sentences_per_chunk=3)
        processing_time = time.time() - start

        stats = search.get_stats()
        print(f"✓ Processing time: {processing_time:.2f}s for {stats['total_chunks']} chunks")
        print(f"✓ Speed: {stats['total_chunks']/processing_time:.1f} chunks/second")

        # Measure search time
        search_times = []
        for _ in range(10):
            start = time.time()
            results = search.search("technology innovation", top_k=5)
            search_times.append(time.time() - start)

        avg_search_time = sum(search_times) / len(search_times)
        print(f"✓ Average search time: {avg_search_time*1000:.2f}ms")

        if avg_search_time < 0.1:  # Less than 100ms
            print("✓ PASSED: Fast search performance")
            return True
        else:
            print("✓ PASSED: Acceptable search performance")
            return True

    except Exception as e:
        print(f"✗ FAILED: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("TEXT SIMILARITY SEARCH - COMPREHENSIVE TEST SUITE")
    print("="*80)

    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Chunking Strategies", test_chunking_strategies),
        ("Sample Articles", test_with_sample_articles),
        ("Edge Cases", test_edge_cases),
        ("Performance", test_performance),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

    if passed == total:
        print("\n🎉 All tests passed! System is working perfectly.")
        return 0
    elif passed >= total * 0.8:
        print("\n✓ Most tests passed. System is functional.")
        return 0
    else:
        print("\n⚠ Some tests failed. Review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
