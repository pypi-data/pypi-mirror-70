import yaml
import uuid
import base64
from copy import deepcopy, copy

try:
    from aenum import Enum
except ImportError:
    from enum import Enum


class Group(object):
    """
    A non-stored attribute that can be used as a separator of attributes in a
    flat-stored structure.
    """
    def __init__(self):
        self._structure = None  # type: structured_config.Structure
        self._fields = []

    def __register_structure__(self, structure):
        self._structure = structure

    def __update__(self):
        if not self._fields:
            adding = False
            for k, v in self._structure.__dict__.items():
                if not adding:
                    if v is self:
                        adding = True
                else:
                    if isinstance(v, Group):
                        break
                    self._fields.append(k)

    def __getattr__(self, item):
        if item in ('_fields', '_structure'):
            return super(Group, self).__getattr__(item)
        self.__update__()
        if not item in self._fields:
            raise AttributeError()
        return getattr(self._structure, item)

    def __setattr__(self, key, value):
        if key in ('_fields', '_structure'):
            return super(Group, self).__setattr__(key, value)
        self.__update__()
        if not key in self._fields:
            raise AttributeError()
        return setattr(self._structure, key, value)

    __setitem__ = __setattr__
    __getitem__ = __getattr__

    def __len__(self):
        self.__update__()
        return len(self._fields)

    def __dir__(self):
        self.__update__()
        return self._fields

    def __iter__(self):
        self.__update__()
        for key in self._fields:
            yield key, getattr(self._structure, key)

    def __deepcopy__(self, memodict={}):
        o = Group()
        o._fields = self._fields
        o._structure = self._structure
        return o


class Field(object):
    """
    Base class for fields that allows capturing of comments or'ed with the field
    """
    def __init__(self, value):
        self.__doc__ = ""
        self.__group__ = ""
        self.value = value

    def __or__(self, other):
        self.__doc__ = other
        return self

    def __getstate__(self):
        return self.value

    def __setstate__(self, state):
        self.value = state

    def __deepcopy__(self, memodict=None):
        n = self.__class__(deepcopy(self.value, memodict or {}))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n


class TypedField(Field):
    def __init__(self, value, converter, store_converted=True, writer=None, **kwargs):
        self.converter = converter
        self.writer = writer if writer else converter
        self.store_converted = store_converted
        super(TypedField, self).__init__(value=value)

        cls = self.__class__
        self._yaml_tag = '!' + cls.__name__

        yaml.add_constructor(self._yaml_tag, self._from_yaml)

    def __deepcopy__(self, memodict=None):
        if self.__class__ is TypedField:
            n = self.__class__(deepcopy(self.value, memodict or {}), self.converter, self.store_converted, self.writer)
        else:
            n = self.__class__(deepcopy(self.value, memodict or {}))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    @classmethod
    def _from_yaml(cls, loader, node):
        return loader.construct_yaml_object(node, cls)


class Deprecated(TypedField):
    def __init__(self, field, new_fieldname=None, converter=None):
        """
        This is used as a wrapper to denote a field as deprecated.
        When the field is read from yaml it will be run through converter to convert contents
        to new field if needed.
        This field cannot be read by the software end-use any longer and will not be written back to yaml
        :param Field field: Original field declaration
        :param str new_fieldname:  name of the new target field the converted output should be stored in
        :param function converter: function/lambda to convert to new field
        """
        if new_fieldname is not None and not isinstance(new_fieldname, str):
            raise ValueError("new_fieldname arg must be the name of the converted target field")
        self.new_fieldname = new_fieldname

        if isinstance(field, Deprecated):
            converter = converter or field._converter
            if field.new_fieldname:
                self.new_fieldname = field.new_fieldname
            field = field.field

        self.field = field
        self._converter = converter
        self.structure = None  # type: structured_config.Structure
        try:
            value = field.value
        except AttributeError:
            value = field
        super(Deprecated, self).__init__(value, self.converter)

    def __register_structure__(self, structure):
        self.structure = structure

    def converter(self, value):
        if self._converter:
            value = self._converter(value)
        if self.new_fieldname:
            if self.structure:
                setattr(self.structure, self.new_fieldname, value)
        else:
            self.field.value = value
        return value

    @property
    def value(self):
        if self.structure:
            import warnings
            msg = "Field deprecated"
            if self.new_fieldname:
                msg += ", please change to %s" % self.new_fieldname
            warnings.warn(msg, category=DeprecationWarning, stacklevel=1)
        if isinstance(self.field, TypedField):
            return self.field.converter(self.field.value)
        return self.field.value

    @value.setter
    def value(self, val):
        if isinstance(self.field, TypedField):
            val = self.field.converter(val)
        self.converter(val)

    def __deepcopy__(self, memodict=None):
        n = self.__class__(*deepcopy((self.field, self.new_fieldname, self._converter), memodict or {}))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n

    def __setstate__(self, state):
        self.value = state


class IntField(TypedField):
    def __init__(self, value):
        super(IntField, self).__init__(value, lambda v: None if v is None else int(v))


class StrField(TypedField):
    def __init__(self, value):
        super(StrField, self).__init__(value, lambda v: None if v is None else str(v))


class FloatField(TypedField):
    def __init__(self, value):
        super(FloatField, self).__init__(value, self.__check__)

    @staticmethod
    def __check__(value):
        if value is None:
            return None
        if (value * 0) != 0:  # test for nan/inf:
            return "nan"
        return float(value)


class PathField(TypedField):
    def __init__(self, value):
        try:
            from pathlib import Path
        except ImportError:
            from pathlib2 import Path
        super(PathField, self).__init__(value, Path)


class RangedNumber(TypedField):
    def __init__(self, value, min, max):
        self.min = min
        self.max = max
        super(RangedNumber, self).__init__(value, self.__check__)

    def __check__(self, value):
        if self.min <= value <= self.max:
            return value
        raise ValueError("%s out of range (%s - %s)" % (value, self.min, self.max))

    def update_range(self, min, max):
        self.min = min
        self.max = max

    def __repr__(self):
        return "<RangedInt:%s<=%s<=%s>" % (self.min, self.value, self.max)

    def __deepcopy__(self, memodict=None):
        n = self.__class__(*deepcopy((self.value, self.min, self.max), memodict or {}))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n


class RangedFloat(RangedNumber):
    def __check__(self, value):
        try:
            return super(RangedFloat, self).__check__(float(value))
        except TypeError:
            raise ValueError("%s out of range (%s - %s)" % (value, self.min, self.max))


class RangedInt(RangedNumber):
    def __check__(self, value):
        try:
            return super(RangedInt, self).__check__(int(value))
        except TypeError:
            raise ValueError("%s out of range (%s - %s)" % (value, self.min, self.max))


class RangedInts(RangedInt):
    def __check__(self, values):
        return [super(RangedInts, self).__check__(value) for value in values]


class BoolField(TypedField):
    def __init__(self, value):
        super(BoolField, self).__init__(value, self.to_bool)

    @staticmethod
    def to_bool(val):
        if isinstance(val, str):
            val = val.lower() in ['yes', 'true']
        else:
            val = True if val else False
        return val


class Selection(str, Enum):
    def __init__(self, *_, **__):
        self._value_ = self.name
        str.__init__(self)

    def __deepcopy__(self, memodict=None):
        """Enums are immutable, so it's safe for deepcopy to return self
        """
        return self

    def __copy__(self):
        return self

    def __str__(self):
        return self._value_

    def __eq__(self, other):
        return self is other or str(other) == self._value_


class SelectionField(TypedField):
    def __init__(self, value, allowed_values):
        """
        Enforces the value to be one of the allowed values
        :param str|property value:
        :param List[str] | Type[Selection] allowed_values: the list of allowed values
        """
        if isinstance(allowed_values, list):
            allowed_values = Selection('Selection', allowed_values)
        self.allowed_values = allowed_values
        super(SelectionField, self).__init__(value, self.check)

    def check(self, val):
        return self.allowed_values[str(val)].name

    def __deepcopy__(self, memodict=None):
        n = self.__class__(copy(self.value), copy(self.allowed_values))
        n.__doc__ = self.__doc__
        n.__group__ = self.__group__
        return n


class MultiSelection(SelectionField):
    def __init__(self, values, allowed_values):
        """
        Enforces the values to be in the allowed values
        :param list|tuple values: list of values which all need to be allowed
        :param List[str] | Type[Selection] allowed_values: the list of allowed values
        """
        super(MultiSelection, self).__init__(tuple(values), allowed_values)

    def check(self, vals):
        return tuple((super(MultiSelection, self).check(val) for val in vals))


class EncryptedField(TypedField):
    PASSWORD = None
    crypt_header = b'ENC:'

    def __init__(self, value, password=None):
        try:
            import cryptography
        except ImportError:
            raise ImportError("Must install 'cryptography' package to use EncryptedField")

        self.password = password
        super(EncryptedField, self).__init__(value=value, converter=self.decrypt, writer=self.encrypt)
        self._coders = {}  # cache

    @property
    def _password(self):
        return self.password or self.PASSWORD

    @property
    def _crypt(self):
        """
        :param str password:
        :return: fernet.Fernet
        """
        from cryptography import fernet
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

        if self._password in self._coders:
            return self._coders[self._password]

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=uuid.uuid5(uuid.NAMESPACE_OID, 'gitlab_runner_manager').bytes,
            iterations=10000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(self._password.encode()
                                                  if isinstance(self._password, str) else self._password))
        f = fernet.Fernet(key)
        self._coders[self._password] = f
        return f

    def encrypt(self, data):
        bdata = data.encode() if isinstance(data, str) else data
        if data is None or bdata.startswith(self.crypt_header):
            return data
        return (self.crypt_header + self._crypt.encrypt(bdata)).decode()

    def decrypt(self, data):
        bdata = data.encode() if isinstance(data, str) else data
        if data is None or not bdata.startswith(self.crypt_header):
            return data
        return (self._crypt.decrypt(bdata[len(self.crypt_header):])).decode()
