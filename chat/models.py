from dataclasses import dataclass
from datetime import datetime

@dataclass
class Message:
    sender_id: str
    receiver_id: str
    content: str
    timestamp: str

    @staticmethod
    def create(sender_id, receiver_id, content):
        return Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            timestamp=datetime.utcnow().isoformat()
        )

