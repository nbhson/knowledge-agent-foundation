def test_fencing():
    assert accept_result(token=5, current=6, attempt=1) is False
    assert accept_result(token=6, current=6, attempt=1) is True
    assert accept_result(token=6, current=6, attempt=4) is False

def test_cas():
    b = Blackboard()
    assert b.write("a/T-1/x", "v1", 0, "a") is True
    assert b.write("a/T-1/x", "v2-stale", 0, "a") is False
