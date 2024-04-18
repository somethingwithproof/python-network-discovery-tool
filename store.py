import json
import logging
from typing import Any, Dict

# Setup logging
logger = logging.getLogger(__name__)

class DataStore:
    """Manages storing and retrieving data to and from a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Dict[str, Any] = self.load_data()

    def load_data(self) -> Dict[str, Any]:
        """Loads data from the JSON file."""
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.warning(f"File {self.file_path} not found. Creating a new one.")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}")
            return {}

    def save_data(self) -> None:
        """Saves data to the JSON file."""
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get(self, key: str) -> Any:
        """Gets the value associated with a key."""
        return self.data.get(key)

    def set(self, key: str, value: Any) -> None:
        """Sets the value for a key."""
        self.data[key] = value
        self.save_data()

    def delete(self, key: str) -> None:
        """Deletes a key from the data store."""
        if key in self.data:
            del self.data[key]
            self.save_data()
