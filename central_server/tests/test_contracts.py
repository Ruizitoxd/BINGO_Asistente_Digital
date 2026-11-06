import pytest
from pydantic import ValidationError

from app.schemas.contracts import (
    CommandRequest, CommandStatus, DeviceDescriptor, DeviceType, EventEnvelope
)


def test_command_request_generates_id():
    item = CommandRequest(
        device_id="android_poco_f7", module="navigation",
        action="start_navigation", parameters={"destination": "Centro"}
    )
    assert item.request_id
    assert item.device_id == "android_poco_f7"


def test_command_request_rejects_extra_fields():
    with pytest.raises(ValidationError):
        CommandRequest(
            device_id="phone", module="navigation",
            action="start", unexpected_field=True
        )


def test_device_descriptor():
    item = DeviceDescriptor(
        device_id="windows_laptop", device_type=DeviceType.WINDOWS,
        display_name="Portátil Windows"
    )
    assert item.device_type == DeviceType.WINDOWS


def test_event_schema_version():
    event = EventEnvelope(event_type="device.connected", source_device_id="phone")
    assert event.schema_version == "1.0"


def test_status_enum():
    assert CommandStatus.SUCCESS.value == "success"
