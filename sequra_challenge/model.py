from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class LaunchCore(BaseModel):
    launch_id: str
    core: Optional[str]
    flight: Optional[int]
    gridfins: Optional[bool]
    legs: Optional[bool]
    reused: Optional[bool]
    landing_attempt: Optional[bool]
    landing_success: Optional[bool]
    landing_type: Optional[str]
    landpad: Optional[str]


class LaunchCrew(BaseModel):
    launch_id: str
    crew: str
    role: str


# TODO haven't been able to make Json fields work inside a
# complex model with psycopg2. They do work as standalone 1 field
class Launch(BaseModel):
    # fairings: Optional[Json]
    # links: Optional[Json]
    static_fire_date_utc: Optional[str]
    static_fire_date_unix: Optional[int]
    tdb: Optional[bool] = None
    net: bool
    window: Optional[int]
    rocket: str
    success: Optional[bool]
    # failures: Optional[Json]
    details: Optional[str]
    ships: list[str]
    # capsules: Optional[Json]
    # payloads: Optional[Json]
    launchpad: str
    auto_update: bool
    flight_number: int
    name: str
    date_utc: str
    date_unix: int
    date_local: str
    date_precision: str
    upcoming: bool
    auto_update: bool
    tbd: bool
    launch_library_id: Optional[str]
    id: str
