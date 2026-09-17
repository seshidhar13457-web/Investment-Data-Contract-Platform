from vendor_poc.gable.impact_analyzer import analyze_field_change


def test_investor_id_is_breaking():
    result = analyze_field_change("investor_id")
    assert result == 1


def test_price_is_breaking():
    result = analyze_field_change("price")
    assert result == 1


def test_trade_id_is_breaking():
    result = analyze_field_change("trade_id")
    assert result == 1


def test_broker_code_has_no_registered_consumer_impact():
    result = analyze_field_change("broker_code")
    assert result == 0