from datetime import date
from astral import moon


class AstronomyService:
    """Calculates moon phase locally."""

    def get_moon_phase(self, target_date: date | None = None) -> dict:
        target_date = target_date or date.today()
        phase_index = moon.phase(target_date)

        if phase_index < 1.84 or phase_index >= 27.68:
            name = "New Moon"
        elif phase_index < 5.53:
            name = "Waxing Crescent"
        elif phase_index < 9.22:
            name = "First Quarter"
        elif phase_index < 12.91:
            name = "Waxing Gibbous"
        elif phase_index < 16.61:
            name = "Full Moon"
        elif phase_index < 20.30:
            name = "Waning Gibbous"
        elif phase_index < 23.99:
            name = "Last Quarter"
        else:
            name = "Waning Crescent"

        return {
            "date": target_date.isoformat(),
            "phase_index": round(phase_index, 2),
            "phase_name": name,
        }


astronomy_service = AstronomyService()