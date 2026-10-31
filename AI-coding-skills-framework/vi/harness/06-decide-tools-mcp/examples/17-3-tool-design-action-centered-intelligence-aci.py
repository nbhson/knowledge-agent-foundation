# ❌ BAD: Description mơ hồ
{
    "name": "get_data",
    "description": "Lấy dữ liệu từ hệ thống",
}

# ✅ GOOD: Description như docstring dev
{
    "name": "get_employee_records",
    "description": """
    Trả về danh sách nhân viên theo filter.
    Args:
        department (str): Tên phòng ban (VD: "IT", "HR")
        status (str): Trạng thái ("active"|"all", default="active")
        limit (int): Số bản ghi tối đa (1-100, default=50)
    Returns:
        List[dict]: Danh sách nhân viên với fields: id, name, department, email
    Raises:
        ValueError: department không hợp lệ
        PermissionError: Không có quyền truy cập phòng ban này
    """,
}
