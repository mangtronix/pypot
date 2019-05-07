from .abstract_io import AbstractDxlIO, _DxlControl, _DxlAccess
from .. import conversion as conv
from ..protocol import v2


class DxlXMIO(AbstractDxlIO):
    _protocol = v2


controls = {
    # EEPROM
    'model': {
        'address': 0x00,
        'access': _DxlAccess.readonly,
        'dxl_to_si': conv.dxl_to_model
    },
    # RAM
    'torque_enable': {
        'address': 64,
        'length': 1,
        'dxl_to_si': conv.dxl_to_bool,
        'si_to_dxl': conv.bool_to_dxl,
        'getter_name': 'is_torque_enabled',
        'setter_name': '_set_torque_enable'
    },
    'goal position': {
        'address': 116,
        'length': 4,
        'dxl_to_si': conv.dxl_to_degree,
        'si_to_dxl': conv.degree_to_dxl
    },
    'present position': {
        'address': 132,
        'length': 4,
        'access': _DxlAccess.readonly,
        'dxl_to_si': conv.dxl_to_degree
    },
    'present temperature': {
        'address': 146,
        'length': 1,
        'access': _DxlAccess.readonly,
        'dxl_to_si': conv.dxl_to_temperature
    },
}


def _add_control(name,
                 address, length=2, nb_elem=1,
                 access=_DxlAccess.readwrite,
                 models=['XM430-W350', 'XM430-W210'],
                 dxl_to_si=lambda val, model: val,
                 si_to_dxl=lambda val, model: val,
                 getter_name=None,
                 setter_name=None):

    control = _DxlControl(name,
                          address, length, nb_elem,
                          access,
                          models,
                          dxl_to_si, si_to_dxl,
                          getter_name, setter_name)

    DxlXMIO._generate_accessors(control)


for name, args in controls.items():
    _add_control(name, **args)
