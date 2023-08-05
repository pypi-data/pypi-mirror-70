import decimal
import uuid
from datetime import datetime, timezone

from schematizer.schemas.base import BaseCoercibleSchema, BaseSchema


class Dummy(BaseSchema):
    def to_native(self, obj):
        return obj

    def to_primitive(self, obj):
        return obj


class Bool(BaseCoercibleSchema):
    TRUE_VALUES = (True, 1, '1', 'true', 't', 'yes', 'y', 'on')
    FALSE_VALUES = (False, 0, '0', 'false', 'f', 'no', 'n', 'off')

    def coerce_primitive(self, obj):
        if obj in self.TRUE_VALUES:
            return True
        if obj in self.FALSE_VALUES:
            return False
        else:
            raise ValueError(f'not a boolean: {obj!r}')

    coerce_native = bool


class Int(BaseCoercibleSchema):
    coerce_primitive = int
    coerce_native = int


class Float(BaseCoercibleSchema):
    coerce_primitive = float
    coerce_native = float


class Str(BaseCoercibleSchema):
    def __init__(self, strip=False):
        super().__init__()
        self.strip = strip

    def coerce(self, obj):
        str_obj = str(obj)
        return str_obj.strip() if self.strip else str_obj

    coerce_primitive = coerce
    coerce_native = coerce


class Decimal(BaseCoercibleSchema):
    coerce_primitive = decimal.Decimal

    def coerce_native(self, obj):
        return f'{obj.normalize():f}'


class UUID(BaseCoercibleSchema):
    coerce_primitive = uuid.UUID
    coerce_native = str


class DateTime(BaseCoercibleSchema):
    def coerce_primitive(self, obj):
        return datetime.utcfromtimestamp(float(obj))

    def coerce_native(self, obj):
        return obj.replace(tzinfo=timezone.utc).timestamp()


class Enum(BaseCoercibleSchema):
    def __init__(self, enum_type):
        super().__init__()
        self.enum_type = enum_type

    def coerce_primitive(self, obj):
        return self.enum_type(obj)

    def coerce_native(self, obj):
        return self.enum_type(obj).value
