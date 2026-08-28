import pytest
from worker import EventWorker

@pytest.fixture
def worker():
    return EventWorker()

def test_valid_event_processing(worker):
    valid_json = '{"event_type": "USER_REGISTERED", "data": {"user_id": 42}}'
    success = worker.process_message(valid_json)
    assert success is True
    assert len(worker.processed_events) == 1
    assert len(worker.dead_letter_queue) == 0
    assert worker.processed_events[0]["event_type"] == "USER_REGISTERED"

def test_invalid_json_routing_to_dlq(worker):
    invalid_json = '{"event_type": "USER_REGISTERED", broken_json'
    success = worker.process_message(invalid_json)
    assert success is False
    assert len(worker.processed_events) == 0
    assert len(worker.dead_letter_queue) == 1
    assert "Invalid JSON format" in worker.dead_letter_queue[0]["error"]

def test_missing_fields_routing_to_dlq(worker):
    missing_fields_json = '{"user_id": 42}'
    success = worker.process_message(missing_fields_json)
    assert success is False
    assert len(worker.processed_events) == 0
    assert len(worker.dead_letter_queue) == 1
    assert "Missing required fields" in worker.dead_letter_queue[0]["error"]

def test_non_dict_json_routing_to_dlq(worker):
    array_json = '["event1", "event2"]'
    success = worker.process_message(array_json)
    assert success is False
    assert len(worker.dead_letter_queue) == 1