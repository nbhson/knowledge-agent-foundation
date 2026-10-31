import numpy as np

# ============================================================
# 1. COSINE SIMILARITY (Phổ biến nhất)
# ============================================================
# Đo GÓC giữa 2 vector, KHÔNG phụ thuộc vào độ dài

def cosine_similarity(a, b):
    """
    a, b: vector (list hoặc numpy array)
    Returns: float [-1, 1]
    
    1.0  = Hoàn toàn giống nhau
    0.0  = Không liên quan
    -1.0 = Hoàn toàn đối lập
    """
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Ví dụ:
# "Chó"     → [0.9, 0.1, 0.2]
# "Mèo"     → [0.85, 0.15, 0.25]  # cosine_sim = 0.99 (gần nhau)
# "Xe hơi"  → [0.1, 0.8, 0.3]     # cosine_sim = 0.45 (xa nhau)


# ============================================================
# 2. DOT PRODUCT
# ============================================================
# Đơn giản nhất, CHỈ dùng khi vectors đã được normalize

def dot_product_similarity(a, b):
    """
    Nếu vectors đã normalize → dot product = cosine similarity
    Nếu KHÔNG normalize → phụ thuộc vào magnitude
    """
    return np.dot(np.array(a), np.array(b))


# ============================================================
# 3. EUCLIDEAN DISTANCE (L2)
# ============================================================
# Đo KHOẢNG CÁCH thực tế giữa 2 điểm

def euclidean_distance(a, b):
    """
    Nhỏ hơn = Gần hơn
    0 = Giống hệt
    
    Lưu ý: Phụ thuộc vào magnitude (chiều dài vector)
    """
    a, b = np.array(a), np.array(b)
    return np.linalg.norm(a - b)


# ============================================================
# 4. MANHATTAN DISTANCE (L1)
# ============================================================
# Tổng khoảng cách theo từng chiều

def manhattan_distance(a, b):
    """
    Tính tổng |a_i - b_i| cho tất cả chiều i
    Ít nhạy hơn với outliers so với L2
    """
    return np.sum(np.abs(np.array(a) - np.array(b)))


# ============================================================
# 5. MUTUAL INFORMATION SCORE
# ============================================================
# Dùng cho sparse vectors (BM25, TF-IDF)
# Không dùng cho dense vectors
