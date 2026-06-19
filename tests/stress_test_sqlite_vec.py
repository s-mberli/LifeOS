import sqlite3
import struct
import random
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.db import get_db_connection, init_db

def serialize_float32(vector):
    return struct.pack("%sf" % len(vector), *vector)

def test_run_stress_test():
    print("Connecting to in-memory database...")
    conn = get_db_connection(":memory:")
    
    print("Initializing DB schema...")
    init_db(conn)
    
    cursor = conn.cursor()
    
    # Generate sample vector data (768 dimensions)
    # We will insert 100 vectors
    print("Generating 100 sample vectors of 768 dimensions...")
    vectors = []
    for i in range(100):
        vec = [random.uniform(-1.0, 1.0) for _ in range(768)]
        # normalize to make cosine distance simpler
        norm = sum(x*x for x in vec) ** 0.5
        vec = [x/norm for x in vec]
        vectors.append(vec)
        
    print("Inserting vector data into vec_docs and doc_chunks...")
    for i, vec in enumerate(vectors):
        cursor.execute(
            "INSERT INTO doc_chunks (id, path, chunk_index, content) VALUES (?, ?, ?, ?)",
            (i + 1, f"doc_{i}.md", i, f"Content of document chunk {i}")
        )
        
        serialized = serialize_float32(vec)
        cursor.execute(
            "INSERT INTO vec_docs (rowid, embedding) VALUES (?, ?)",
            (i + 1, serialized)
        )
    
    conn.commit()
    print("Data inserted successfully.")
    
    # Query vector
    query_vector = vectors[0]
    serialized_query = serialize_float32(query_vector)
    
    print("Running KNN search using vec_distance_cosine()...")
    cursor.execute("""
        SELECT 
            rowid,
            distance
        FROM vec_docs
        WHERE embedding MATCH ? AND k = 5
    """, (serialized_query,))
    
    results = cursor.fetchall()
    print(f"KNN search found {len(results)} matches:")
    for row in results:
        rowid = row[0]
        dist = row[1]
        print(f"  RowID: {rowid}, Distance: {dist:.6f}")
        
    # Assertions
    assert len(results) == 5, f"Expected 5 results, got {len(results)}"
    first_rowid = results[0][0]
    first_dist = results[0][1]
    assert first_rowid == 1, f"Expected closest to be rowid 1, got {first_rowid}"
    assert abs(first_dist) < 1e-5, f"Expected distance to be close to 0, got {first_dist}"
    
    # Mismatched dimension tests
    print("Testing adversarial inputs (dimension mismatch)...")
    
    # 1. Insertion mismatch (767 dimensions instead of 768)
    invalid_vec_small = [random.uniform(-1.0, 1.0) for _ in range(767)]
    serialized_invalid_small = serialize_float32(invalid_vec_small)
    try:
        cursor.execute(
            "INSERT INTO vec_docs (rowid, embedding) VALUES (?, ?)",
            (101, serialized_invalid_small)
        )
        assert False, "Expected sqlite3.OperationalError for 767-dimension insert, but it succeeded"
    except sqlite3.OperationalError as e:
        print(f"  Passed: 767-dim insert failed as expected with error: {e}")
        
    # 2. Insertion mismatch (769 dimensions instead of 768)
    invalid_vec_large = [random.uniform(-1.0, 1.0) for _ in range(769)]
    serialized_invalid_large = serialize_float32(invalid_vec_large)
    try:
        cursor.execute(
            "INSERT INTO vec_docs (rowid, embedding) VALUES (?, ?)",
            (102, serialized_invalid_large)
        )
        assert False, "Expected sqlite3.OperationalError for 769-dimension insert, but it succeeded"
    except sqlite3.OperationalError as e:
        print(f"  Passed: 769-dim insert failed as expected with error: {e}")

    # 3. Query mismatch (767 dimensions instead of 768)
    try:
        cursor.execute("""
            SELECT rowid, distance
            FROM vec_docs
            WHERE embedding MATCH ? AND k = 5
        """, (serialized_invalid_small,))
        cursor.fetchall()
        assert False, "Expected sqlite3.OperationalError for 767-dimension KNN search, but it succeeded"
    except sqlite3.OperationalError as e:
        print(f"  Passed: 767-dim KNN search failed as expected with error: {e}")

    print("KNN search stress test PASSED successfully!")
    conn.close()

if __name__ == "__main__":
    run_stress_test()
