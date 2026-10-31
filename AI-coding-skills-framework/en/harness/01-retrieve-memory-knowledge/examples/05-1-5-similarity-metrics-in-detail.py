import numpy as np

# ============================================================
# 1. COSINE SIMILARITY (The most common)
# ============================================================
# Measures the ANGLE between two vectors, NOT dependent on length

def cosine_similarity(a, b):
    """
    a, b: vectors (list or numpy array)
    Returns: float [-1, 1]

    1.0  = Completely identical
    0.0  = Unrelated
    -1.0 = Completely opposite
    """
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Example:
# "Dog"     → [0.9, 0.1, 0.2]
# "Cat"     → [0.85, 0.15, 0.25]  # cosine_sim = 0.99 (close)
# "Car"     → [0.1, 0.8, 0.3]     # cosine_sim = 0.45 (far)


# ============================================================
# 2. DOT PRODUCT
# ============================================================
# The simplest; ONLY use when the vectors are already normalized

def dot_product_similarity(a, b):
    """
    If the vectors are normalized → dot product = cosine similarity
    If NOT normalized → depends on magnitude
    """
    return np.dot(np.array(a), np.array(b))


# ============================================================
# 3. EUCLIDEAN DISTANCE (L2)
# ============================================================
# Measures the actual DISTANCE between two points

def euclidean_distance(a, b):
    """
    Smaller = Closer
    0 = Identical

    Note: Depends on magnitude (vector length)
    """
    a, b = np.array(a), np.array(b)
    return np.linalg.norm(a - b)


# ============================================================
# 4. MANHATTAN DISTANCE (L1)
# ============================================================
# Sum of distances along each dimension

def manhattan_distance(a, b):
    """
    Sums up |a_i - b_i| over all dimensions i
    Less sensitive to outliers than L2
    """
    return np.sum(np.abs(np.array(a) - np.array(b)))


# ============================================================
# 5. MUTUAL INFORMATION SCORE
# ============================================================
# Used for sparse vectors (BM25, TF-IDF)
# Not used for dense vectors
