import re
from datetime import datetime

class WhatsAppParser:
    """
    Parses a WhatsApp exported chat .txt file into structured message records.
    """

    # WhatsApp message pattern: "12/31/21, 11:59 PM - Name: Message"
    message_pattern = re.compile(
        r"^(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2} (?:AM|PM)) - (.*?): (.*)$"
    )

    def parse(self, filepath):
        messages = []
        with open(filepath, encoding="utf-8") as f:
            current_message = None
            for line in f:
                line = line.strip()
                match = self.message_pattern.match(line)
                if match:
                    # Save previous message if continuing
                    if current_message:
                        messages.append(current_message)
                    date_str, time_str, sender, text = match.groups()
                    try:
                        timestamp = datetime.strptime(f"{date_str} {time_str}", "%m/%d/%y %I:%M %p")
                    except ValueError:
                        try:
                            timestamp = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%y %I:%M %p")
                        except ValueError:
                            continue
                    current_message = {
                        "timestamp": timestamp.isoformat(),
                        "sender": sender,
                        "text": text
                    }
                else:
                    # Continuation of previous message
                    if current_message:
                        current_message["text"] += " " + line
            if current_message:
                messages.append(current_message)
        return messages
