from datetime import datetime, date
from enum import Enum
from typing import List, Optional

class PestType(Enum):
    RODENT = "rodent"
    INSECT = "insect"
    BIRD = "bird"
    REPTILE = "reptile"
    OTHER = "other"

class SeverityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TreatmentStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Location:
    def __init__(self, name: str, address: str, coordinates: Optional[tuple] = None):
        self.id = id(self)
        self.name = name
        self.address = address
        self.coordinates = coordinates  # (latitude, longitude)
        self.created_at = datetime.now()

class Pest:
    def __init__(self, name: str, pest_type: PestType, description: str = ""):
        self.id = id(self)
        self.name = name
        self.pest_type = pest_type
        self.description = description
        self.created_at = datetime.now()

class PestSighting:
    def __init__(self, pest: Pest, location: Location, severity: SeverityLevel, 
                 description: str = "", photo_path: Optional[str] = None):
        self.id = id(self)
        self.pest = pest
        self.location = location
        self.severity = severity
        self.description = description
        self.photo_path = photo_path
        self.sighting_date = datetime.now()
        self.reported_by = ""

class Treatment:
    def __init__(self, pest_sighting: PestSighting, method: str, 
                 scheduled_date: date, cost: float = 0.0):
        self.id = id(self)
        self.pest_sighting = pest_sighting
        self.method = method
        self.scheduled_date = scheduled_date
        self.actual_date = None
        self.cost = cost
        self.status = TreatmentStatus.PENDING
        self.notes = ""
        self.effectiveness_rating = None  # 1-5 scale

class Inspection:
    def __init__(self, location: Location, inspector_name: str):
        self.id = id(self)
        self.location = location
        self.inspector_name = inspector_name
        self.inspection_date = datetime.now()
        self.findings = []  # List of PestSighting objects
        self.notes = ""
        self.next_inspection_date = None

class PestTracker:
    def __init__(self):
        self.locations = []
        self.pests = []
        self.sightings = []
        self.treatments = []
        self.inspections = []
    
    def add_location(self, name: str, address: str, coordinates: Optional[tuple] = None) -> Location:
        location = Location(name, address, coordinates)
        self.locations.append(location)
        return location
    
    def add_pest(self, name: str, pest_type: PestType, description: str = "") -> Pest:
        pest = Pest(name, pest_type, description)
        self.pests.append(pest)
        return pest
    
    def log_sighting(self, pest: Pest, location: Location, severity: SeverityLevel,
                    description: str = "", photo_path: Optional[str] = None) -> PestSighting:
        sighting = PestSighting(pest, location, severity, description, photo_path)
        self.sightings.append(sighting)
        return sighting
    
    def schedule_treatment(self, pest_sighting: PestSighting, method: str,
                          scheduled_date: date, cost: float = 0.0) -> Treatment:
        treatment = Treatment(pest_sighting, method, scheduled_date, cost)
        self.treatments.append(treatment)
        return treatment
    
    def create_inspection(self, location: Location, inspector_name: str) -> Inspection:
        inspection = Inspection(location, inspector_name)
        self.inspections.append(inspection)
        return inspection
    
    def get_active_infestations(self) -> List[PestSighting]:
        return [s for s in self.sightings if s.severity in [SeverityLevel.HIGH, SeverityLevel.CRITICAL]]
    
    def get_pending_treatments(self) -> List[Treatment]:
        return [t for t in self.treatments if t.status == TreatmentStatus.PENDING]
    
    def get_location_history(self, location: Location) -> List[PestSighting]:
        return [s for s in self.sightings if s.location.id == location.id]