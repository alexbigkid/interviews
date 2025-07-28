"""
Singleton Pattern - Ensures only one instance of a class exists
Common interview question: Thread-safe singleton implementation
"""

import threading


class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.data = []
            self.initialized = True


class DatabaseConnection(Singleton):
    def connect(self):
        return "Connected to database"
    
    def query(self, sql):
        return f"Executing: {sql}"


# Usage example
if __name__ == "__main__":
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    
    print(f"Same instance: {db1 is db2}")  # True
    print(db1.connect())