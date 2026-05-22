import json
import logging
import sys
from datetime import datetime
from contextvars import ContextVar


trace_id_ctx: ContextVar[str] = ContextVar("trace_id", default="N/A")

class JSONStructuredLogger(logging.Formatter):
    
    def format(self, record: logging.LogRecord) -> str:
        log_payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": self._sanitize_message(record.getMessage()),
            "trace_id": trace_id_ctx.get()
        }
        if record.exc_info:
            log_payload["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_payload)

    def _sanitize_message(self, msg: str) -> str:
        sensitive_keys = ["amount", "transaction_id", "password", "token"]
        for key in sensitive_keys:
            if key in msg.lower():
                return "[SECURE TRANSACTION RECORD] Confidential data masked."
        return msg


logger = logging.getLogger("notification_service")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JSONStructuredLogger())
logger.addHandler(handler)