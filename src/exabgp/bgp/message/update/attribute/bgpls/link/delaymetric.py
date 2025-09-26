# encoding: utf-8
"""
delaymetric.py

Created by (you).
"""

from __future__ import annotations

from struct import unpack

from exabgp.bgp.message.update.attribute.bgpls.linkstate import LinkState
from exabgp.bgp.message.update.attribute.bgpls.linkstate import BaseLS


def _u24(b):
    # Convert 3 bytes (big-endian) to int
    return unpack('!L', b'\x00' + b)[0]


# 1114 - Unidirectional Link Delay (A flag + Reserved + Delay(u24))
@LinkState.register()
class UnidirectionalLinkDelay(BaseLS):
    TLV = 1114
    REPR = 'Unidirectional Link Delay'
    JSON = 'unidirectional-link-delay'
    LEN = 4

    @classmethod
    def unpack(cls, data):
        cls.check(data)
        flags = data[0]
        anomalous = bool(flags & 0x80)
        delay_us = _u24(data[2:5])
        # return a structured value to keep the A-bit
        return cls({'delay-us': delay_us, 'anomalous': anomalous})


# 1115 - Min/Max Unidirectional Link Delay (A + R + Min(u24) + Max(u24))
@LinkState.register()
class MinMaxUnidirectionalLinkDelay(BaseLS):
    TLV = 1115
    REPR = 'Min/Max Unidirectional Link Delay'
    JSON = 'minmax-unidirectional-link-delay'
    LEN = 8

    @classmethod
    def unpack(cls, data):
        cls.check(data)
        flags = data[0]
        anomalous = bool(flags & 0x80)
        min_delay_us = _u24(data[2:5])
        max_delay_us = _u24(data[5:8])
        return cls({
            'min-delay-us': min_delay_us,
            'max-delay-us': max_delay_us,
            'anomalous': anomalous
        })


# 1116 - Unidirectional Delay Variation (R + Variation(u24))
@LinkState.register()
class UnidirectionalDelayVariation(BaseLS):
    TLV = 1116
    REPR = 'Unidirectional Delay Variation'
    JSON = 'unidirectional-delay-variation'
    LEN = 4

    @classmethod
    def unpack(cls, data):
        cls.check(data)
        variation_us = _u24(data[1:4])
        return cls(variation_us)


# 1117 - Unidirectional Link Loss (A + R + Loss(u24) with 0.000003% units)
@LinkState.register()
class UnidirectionalLinkLoss(BaseLS):
    TLV = 1117
    REPR = 'Unidirectional Link Loss'
    JSON = 'unidirectional-link-loss'
    LEN = 4

    _UNIT_PERCENT = 0.000003  # 3e-6 percent per unit

    @classmethod
    def unpack(cls, data):
        cls.check(data)
        flags = data[0]
        anomalous = bool(flags & 0x80)
        enc = _u24(data[2:5])
        loss_percent = enc * cls._UNIT_PERCENT
        return cls({'loss-percent': loss_percent, 'anomalous': anomalous})


# 1118 - Unidirectional Residual Bandwidth (IEEE-754 float, bytes/s)
@LinkState.register()
class UnidirectionalResidualBandwidth(BaseLS):
    TLV = 1118
    REPR = 'Unidirectional Residual Bandwidth'
    JSON = 'unidirectional-residual-bandwidth'
    LEN = 4

    @classmethod
    def unpack(cls, data):
        cls.check(data)
        return cls(unpack('!f', data)[0])


# 1119 - Unidirectional Available Bandwidth (IEEE-754 float, bytes/s)
@LinkState.register()
class UnidirectionalAvailableBandwidth(BaseLS):
    TLV = 1119
    REPR = 'Unidirectional Available Bandwidth'
    JSON = 'unidirectional-available-bandwidth'
    LEN = 4

    @classmethod
    def unpack(cls, data):
        cls.check(data)
        return cls(unpack('!f', data)[0])


# 1120 - Unidirectional Utilized Bandwidth (IEEE-754 float, bytes/s)
@LinkState.register()
class UnidirectionalUtilizedBandwidth(BaseLS):
    TLV = 1120
    REPR = 'Unidirectional Utilized Bandwidth'
    JSON = 'unidirectional-utilized-bandwidth'
    LEN = 4

    @classmethod
    def unpack(cls, data):
        cls.check(data)
        return cls(unpack('!f', data)[0])
