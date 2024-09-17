
class BaseModel:
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ', '.join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{class_name}({properties})"

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)
