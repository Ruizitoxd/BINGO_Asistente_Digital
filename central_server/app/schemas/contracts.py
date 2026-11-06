from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field


class DeviceType(str, Enum):
    ANDROID = "android"
    WINDOWS = "windows"
    SERVER = "server"


class CommandStatus(str, Enum):
    ACCEPTED = "accepted"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    REQUIRES_CONFIRMATION = "requires_confirmation"


class CommandRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str = Field(default_factory=lambda: str(uuid4()))
    device_id: str = Field(min_length=1, max_length=100)
    module: str = Field(min_length=1, max_length=80)
    action: str = Field(min_length=1, max_length=100)
    parameters: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CommandResponse(BaseModel):
    request_id: str
    status: CommandStatus
    message: str
    data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DeviceDescriptor(BaseModel):
    model_config = ConfigDict(extra="forbid")
    device_id: str = Field(min_length=1, max_length=100)
    device_type: DeviceType
    display_name: str = Field(min_length=1, max_length=120)
    protocol_version: str = "1.0"


class EventEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str = Field(min_length=1, max_length=120)
    source_device_id: str = Field(min_length=1, max_length=100)
    payload: dict[str, Any] = Field(default_factory=dict)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    schema_version: str = "1.0"
