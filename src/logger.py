import json
from datetime import datetime
from pathlib import Path

class PredictionLogger:
    """
    Logs predictions to JSONL for analysis.
    JSONL format = one JSON object per line, easy to grep/stream/append.
    """
    
    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
    
    def log(self, entry: dict) -> None:
        entry["timestamp"] = datetime.now().isoformat()
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")