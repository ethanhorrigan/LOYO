import uuid

class UUIDGenerator:

    def generate_uuid():
        id = uuid.uuid1()
        return id.hex