"""Tuya constants."""
from enum import IntEnum, unique


@unique
class CMD_TYPE(IntEnum):
    """Tuya message types."""

    UDP = 0
    AP_CONFIG = 1
    ACTIVE = 2
    BIND = 3
    RENAME_GW = 4
    RENAME_DEVICE = 5
    UNBIND = 6
    CONTROL = 7
    STATUS = 8
    HEART_BEAT = 9
    DP_QUERY = 10
    QUERY_WIFI = 11
    TOKEN_BIND = 12
    CONTROL_NEW = 13
    ENABLE_WIFI = 14
    DP_QUERY_NEW = 16
    SCENE_EXECUTE = 17
    UDP_NEW = 19
    AP_CONFIG_NEW = 20
    LAN_GW_ACTIVE = 240
    LAN_SUB_DEV_REQUEST = 241
    LAN_DELETE_SUB_DEV = 242
    LAN_REPORT_SUB_DEV = 243
    LAN_SCENE = 244
    LAN_PUBLISH_CLOUD_CONFIG = 245
    LAN_PUBLISH_APP_CONFIG = 246
    LAN_EXPORT_APP_CONFIG = 247
    LAN_PUBLISH_SCENE_PANEL = 248
    LAN_REMOVE_GW = 249
    LAN_CHECK_GW_UPDATE = 250
    LAN_GW_UPDATE = 251
    LAN_SET_GW_CHANNEL = 252
    UNKNOWN = -1

    @classmethod
    def _missing_(cls, value):
        return CMD_TYPE.UNKNOWN
