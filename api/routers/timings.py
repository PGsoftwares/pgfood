from fastapi import APIRouter
from apps.partners.models import PartnerRestaurant
from ..schemas import GenericResponse, WorkingHoursUpdateRequest

router = APIRouter(prefix="/restaurant/timings", tags=["7. Restaurant Timing & Working Hours"])


@router.get("")
def get_working_hours():
    """7.1 Get Working Hours."""
    rest = PartnerRestaurant.objects.first()
    if rest and rest.working_days:
        return {
            "workingDays": rest.working_days,
            "openingTime": rest.opening_time,
            "closingTime": rest.closing_time,
            "hasBreakTime": rest.has_break_time,
            "breakStartTime": rest.break_start_time,
            "breakEndTime": rest.break_end_time
        }
    return {
        "workingDays": {
            "Monday": True,
            "Tuesday": True,
            "Wednesday": True,
            "Thursday": True,
            "Friday": True,
            "Saturday": True,
            "Sunday": True
        },
        "openingTime": "10:00",
        "closingTime": "23:30",
        "hasBreakTime": True,
        "breakStartTime": "15:30",
        "breakEndTime": "17:00"
    }


@router.put("", response_model=GenericResponse)
def update_working_hours(payload: WorkingHoursUpdateRequest):
    """7.2 Update Working Hours."""
    rest = PartnerRestaurant.objects.first()
    if rest:
        rest.working_days = payload.workingDays
        rest.opening_time = payload.openingTime
        rest.closing_time = payload.closingTime
        rest.has_break_time = payload.hasBreakTime
        rest.break_start_time = payload.breakStartTime or ""
        rest.break_end_time = payload.breakEndTime or ""
        rest.save()

    return GenericResponse(success=True, message="Operational timings updated successfully")
