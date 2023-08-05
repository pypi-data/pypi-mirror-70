"""EcoNet water heater"""

from datetime import datetime
import logging
from enum import Enum
from typing import List, Union

from pyeconet.equipments import Equipment

_LOGGER = logging.getLogger(__name__)


class WaterHeaterOperationMode(Enum):
    """Define the operation mode"""

    OFF = 1
    ELECTRIC_MODE = 2
    ENERGY_SAVING = 3
    HEAT_PUMP_ONLY = 4
    HIGH_DEMAND = 5
    UNKNOWN = 99

    @staticmethod
    def by_string(str_value: str):
        """Convert a string to a supported OperationMode"""
        _cleaned_string = str_value.rstrip().replace(" ", "_").upper()
        if _cleaned_string == WaterHeaterOperationMode.OFF.name.upper():
            return WaterHeaterOperationMode.OFF
        elif _cleaned_string == WaterHeaterOperationMode.ELECTRIC_MODE.name.upper():
            return WaterHeaterOperationMode.ELECTRIC_MODE
        elif _cleaned_string == WaterHeaterOperationMode.ENERGY_SAVING.name.upper():
            return WaterHeaterOperationMode.ENERGY_SAVING
        elif _cleaned_string == WaterHeaterOperationMode.HEAT_PUMP_ONLY.name.upper():
            return WaterHeaterOperationMode.HEAT_PUMP_ONLY
        elif _cleaned_string == WaterHeaterOperationMode.HIGH_DEMAND.name.upper():
            return WaterHeaterOperationMode.HIGH_DEMAND
        else:
            _LOGGER.error("Unknown mode: [%s]", str_value)
            return WaterHeaterOperationMode.UNKNOWN


class WaterHeater(Equipment):

    def __init__(self, equipment_info: dict, api_interface) -> None:
        """Initialize."""
        super().__init__(equipment_info, api_interface)
        self.energy_usage = None

    @property
    def leak_installed(self) -> bool:
        """Return if heater has leak detection or not"""
        leak = self._equipment_info.get("@LEAKINSTALLED")
        if leak is not None:
            return leak["value"] == 1
        else:
            return False

    @property
    def has_shutoff_valve(self) -> bool:
        return self._equipment_info.get("@VALVE") is not None

    @property
    def running(self) -> bool:
        """Return if the water heater is running or not"""
        return self._equipment_info.get("@RUNNING") == "Running"

    @property
    def tank_hot_water_availability(self) -> Union[int, None]:
        """Return the hot water availability"""
        icon = self._equipment_info.get("@HOTWATER")
        value = 100
        if icon is None:
            _LOGGER.debug("Tank does not support hot water capacity")
            return None
        if icon == "ic_tank_hundread_percent.png":
            value = 100
        elif icon == "ic_tank_fourty_percent.png":
            value = 40
        elif icon == "ic_tank_ten_percent.png":
            value = 10
        elif icon == "ic_tank_empty.png":
            # Tank is empty when shutoff valve is closed
            value = 0
        else:
            _LOGGER.error("Invalid tank level: %s", icon)
        return value

    @property
    def shutoff_valve_open(self) -> bool:
        """Return if the shutoff valve is open or not"""
        return self._equipment_info.get("@VALVE")["value"] == 0

    @property
    def tank_health(self) -> Union[int, None]:
        """Return the value 0-100? of the tank/heating element health"""
        return self._equipment_info.get("@TANK", {}).get("value")

    def _supports_modes(self) -> bool:
        """Return if the system supports modes or not"""
        return self._equipment_info.get("@MODE") is not None

    def _supports_on_off(self) -> bool:
        """Return if the system supports on and off"""
        return self._equipment_info.get("@ENABLED") is not None

    @property
    def modes(self) -> List[WaterHeaterOperationMode]:
        """Return a list of supported operation modes"""
        _supported_modes = []
        if self._supports_modes():
            _modes = self._equipment_info.get("@MODE")["constraints"]["enumText"]
            for _mode in _modes:
                _op_mode = WaterHeaterOperationMode.by_string(_mode)
                if _op_mode is not WaterHeaterOperationMode.UNKNOWN:
                    _supported_modes.append(_op_mode)
        elif self._supports_on_off():
            # This is an electric only water heater supports on/off so...
            _supported_modes = [WaterHeaterOperationMode.OFF, WaterHeaterOperationMode.ELECTRIC_MODE]
        else:
            # Nothing is supported by this unit, return empty list
            _supported_modes = []
        return _supported_modes

    @property
    def mode(self) -> Union[WaterHeaterOperationMode, None]:
        """Return the current mode"""
        if self._supports_modes():
            return self.modes[self._equipment_info.get("@MODE")["value"]]
        else:
            return None

    @property
    def enabled(self) -> bool:
        """Return the the water heater is enabled or not"""
        if self._supports_modes():
            return self.mode != "OFF"
        elif self._supports_on_off():
            return self._equipment_info.get("@ENABLED")["value"] == 1
        else:
            # Unit is always on
            return True


    @property
    def override_status(self) -> str:
        """Return the alert override status"""
        return self._equipment_info.get("@OVERRIDESTATUS")

    @property
    def todays_energy_usage(self) -> Union[float, None]:
        return self.energy_usage

    async def get_energy_usage(self):
        """Call dynamic action for energy usage."""
        date = datetime.now()
        payload = {
            "ACTION": "waterheaterUsageReportView",
            "device_name": f"{self.device_id}",
            "serial_number": f"{self.serial_number}",
            "graph_data": {
                "format": "daily",
                "month": f"{date.month}",
                "period": f"{date.day}",
                "year": f"{date.year}"
            },
            "usage_type": "energyUsage"
        }
        _response = await self._api.get_dynamic_action(payload)
        _todays_usage = 0
        for value in _response["results"]["energy_usage"]["data"]:
            _todays_usage += value["value"]
        self.energy_usage = _todays_usage
        _LOGGER.debug(_todays_usage)

    def set_mode(self, mode: WaterHeaterOperationMode):
        """Set the provided mode or enable/disable if mode isn't support."""
        payload = {}
        if self._supports_modes():
            text_modes = self._equipment_info["@MODE"]["constraints"]["enumText"]
            count = 0
            for text_mode in text_modes:
                if mode == WaterHeaterOperationMode.by_string(text_mode):
                    payload["@MODE"] = count
                count = count + 1
        elif self._supports_on_off():
            if mode == WaterHeaterOperationMode.OFF:
                payload["@ENABLED"] = 0
            else:
                payload["@ENABLED"] = 1
        else:
            _LOGGER.error("Unit doesn't support on off or modes, shouldn't being trying to set a mode.")
        if payload:
            self._api.publish(payload, self.device_id, self.serial_number)
