import json
import logging
from typing import Dict, Any, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RedisWorker")

class EventWorker:
    def __init__(self):
        self.processed_events = []
        self.dead_letter_queue = []

    def parse_event(self, raw_message: str) -> Tuple[bool, Dict[str, Any], str]:
        """Parses raw message string and validates payload schema."""
        try:
            payload = json.loads(raw_message)
            if not isinstance(payload, dict):
                return False, {}, "Payload must be a JSON object"
            if "event_type" not in payload or "data" not in payload:
                return False, payload, "Missing required fields: 'event_type' or 'data'"
            return True, payload, ""
        except json.JSONDecodeError as err:
            return False, {"raw": raw_message}, f"Invalid JSON format: {str(err)}"

    def process_message(self, raw_message: str) -> bool:
        """Processes an incoming raw pub/sub message."""
        is_valid, payload, error_reason = self.parse_event(raw_message)

        if not is_valid:
            logger.warning(f"Routing malformed message to DLQ: {error_reason}")
            self.dead_letter_queue.append({
                "message": payload,
                "error": error_reason
            })
            return False

        logger.info(f"Successfully processed event: {payload['event_type']}")
        self.processed_events.append(payload)
        return True