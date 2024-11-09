class MemoryAgent:
    def __init__(self):
        self.preferences = {}

    def store_preference(self, key, value):
        self.preferences[key] = value

    def get_preference(self, key, default=None):
        return self.preferences.get(key, default)

    def clear_memory(self):
        self.preferences = {}

