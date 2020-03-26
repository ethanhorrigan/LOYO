import uuid

class UUIDGenerator:
    def generate_uuid(self):
        id = uuid.uuid1()
        return id.hex