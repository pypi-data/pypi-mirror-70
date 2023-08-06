# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Protection Authority Bit Assignments"""

from aenum import IntEnum, extend_enum

__all__ = ['ProtectionAuthority']


class ProtectionAuthority(IntEnum):
    """[ProtectionAuthority] Protection Authority Bit Assignments"""

    _ignore_ = 'ProtectionAuthority _'
    ProtectionAuthority = vars()

    ProtectionAuthority['GENSER'] = 0

    ProtectionAuthority['SIOP_ESI'] = 1

    ProtectionAuthority['SCI'] = 2

    ProtectionAuthority['NSA'] = 3

    ProtectionAuthority['DOE'] = 4

    ProtectionAuthority['Unassigned_5'] = 5

    ProtectionAuthority['Unassigned_6'] = 6

    ProtectionAuthority['Field_Termination_Indicator'] = 7

    @staticmethod
    def get(key, default=-1):
        """Backport support for original codes."""
        if isinstance(key, int):
            return ProtectionAuthority(key)
        if key not in ProtectionAuthority._member_map_:  # pylint: disable=no-member
            extend_enum(ProtectionAuthority, key, default)
        return ProtectionAuthority[key]

    @classmethod
    def _missing_(cls, value):
        """Lookup function used when value is not found."""
        if not (isinstance(value, int) and 0 <= value <= 7):
            raise ValueError('%r is not a valid %s' % (value, cls.__name__))
        extend_enum(cls, 'Unassigned [%d]' % value, value)
        return cls(value)
