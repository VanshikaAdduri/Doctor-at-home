import random
from datetime import datetime, timedelta

# ============================================================
# Doctor-at-Home Patient Platform
# CLI-based system where patients register and a doctor
# is automatically assigned and dispatched to their location
# ============================================================

# ============================================================
# CLASS 1: Patient
# Represents a patient requesting home medical visit
# ============================================================
class Patient:
    def __init__(self, patient_id, name, age, location, symptoms):
        self.patient_id = patient_id      # unique ID like PT001
        self.name = name                  # patient name
        self.age = age                    # patient age
        self.location = location          # area in city
        self.symptoms = symptoms          # what they're experiencing
        self.assigned_doctor = None       # will be filled after assignment
        self.appointment_time = None      # will be filled after assignment
        self.status = "waiting"           # waiting / assigned / completed

    def __str__(self):
        return (f"Patient {self.patient_id}: {self.name} | "
                f"Age: {self.age} | "
                f"Location: {self.location} | "
                f"Symptoms: {self.symptoms}")


# ============================================================
# CLASS 2: Doctor
# Represents a doctor available for home visits
# ============================================================
class Doctor:
    def __init__(self, doctor_id, name, specialization, location, available=True):
        self.doctor_id = doctor_id            # unique ID like DR001
        self.name = name                      # doctor name
        self.specialization = specialization  # General / Cardiologist etc
        self.location = location              # area doctor is based in
        self.available = available            # True if free, False if busy
        self.patients_seen = 0               # total patients handled

    def __str__(self):
        status = "Available" if self.available else "Busy"
        return (f"Dr. {self.name} | "
                f"{self.specialization} | "
                f"Location: {self.location} | "
                f"{status}")


# ============================================================
# CLASS 3: Appointment
# Represents a confirmed appointment between patient and doctor
# ============================================================
class Appointment:
    def __init__(self, appointment_id, patient, doctor, time_slot):
        self.appointment_id = appointment_id  # unique ID like APT001
        self.patient = patient                # Patient object
        self.doctor = doctor                  # Doctor object
        self.time_slot = time_slot            # appointment time
        self.status = "confirmed"             # confirmed / completed / cancelled

    def __str__(self):
        return (f"\n  Appointment ID : {self.appointment_id}"
                f"\n  Patient        : {self.patient.name} ({self.patient.location})"
                f"\n  Doctor         : Dr. {self.doctor.name} ({self.doctor.specialization})"
                f"\n  Time Slot      : {self.time_slot}"
                f"\n  Status         : {self.status}")


# ============================================================
# CLASS 4: Platform
# Main system — manages patients, doctors, appointments
# ============================================================
class Platform:
    def __init__(self):
        self.patients = {}          # {patient_id: Patient}
        self.doctors = {}           # {doctor_id: Doctor}
        self.appointments = {}      # {appointment_id: Appointment}
        self.patient_counter = 1    # auto increment patient ID
        self.appointment_counter = 1

    # ── ADD DOCTORS ─────────────────────────────────────────
    def add_doctor(self, name, specialization, location):
        """Register a new doctor on the platform"""
        doctor_id = f"DR{str(len(self.doctors)+1).zfill(3)}"
        doctor = Doctor(doctor_id, name, specialization, location)
        self.doctors[doctor_id] = doctor
        return doctor

    # ── REGISTER PATIENT ────────────────────────────────────
    def register_patient(self, name, age, location, symptoms):
        """Register a new patient and return patient object"""
        patient_id = f"PT{str(self.patient_counter).zfill(3)}"
        self.patient_counter += 1
        patient = Patient(patient_id, name, age, location, symptoms)
        self.patients[patient_id] = patient
        print(f"\n  ✅ Patient registered successfully!")
        print(f"     Patient ID : {patient_id}")
        print(f"     Name       : {name}")
        print(f"     Location   : {location}")
        print(f"     Symptoms   : {symptoms}")
        return patient

    # ── FIND BEST DOCTOR ────────────────────────────────────
    def find_best_doctor(self, patient):
        """
        Find the most suitable available doctor for a patient.

        Priority logic:
        1. Same location as patient (nearest first)
        2. Specialization matching symptoms keywords
        3. Any available doctor as fallback
        """
        available_doctors = [
            d for d in self.doctors.values() if d.available
        ]

        if not available_doctors:
            return None

        # symptom to specialization mapping
        symptom_map = {
            "chest":    "Cardiologist",
            "heart":    "Cardiologist",
            "skin":     "Dermatologist",
            "rash":     "Dermatologist",
            "bone":     "Orthopedist",
            "fracture": "Orthopedist",
            "child":    "Pediatrician",
            "fever":    "General Physician",
            "cold":     "General Physician",
            "cough":    "General Physician",
        }

        # check symptoms for specialization match
        preferred_spec = "General Physician"  # default
        for keyword, spec in symptom_map.items():
            if keyword in patient.symptoms.lower():
                preferred_spec = spec
                break

        # Priority 1: same location + matching specialization
        for doc in available_doctors:
            if (doc.location == patient.location and
                    doc.specialization == preferred_spec):
                return doc

        # Priority 2: same location any specialization
        for doc in available_doctors:
            if doc.location == patient.location:
                return doc

        # Priority 3: matching specialization any location
        for doc in available_doctors:
            if doc.specialization == preferred_spec:
                return doc

        # Priority 4: any available doctor
        return available_doctors[0]

    # ── ASSIGN DOCTOR ────────────────────────────────────────
    def assign_doctor(self, patient):
        """Assign best available doctor to patient"""
        doctor = self.find_best_doctor(patient)

        if not doctor:
            print("\n  ❌ No doctors available right now.")
            print("     Please try again in some time.")
            return None

        # generate time slot — next available hour
        now = datetime.now()
        time_slot = (now + timedelta(hours=1)).strftime("%I:%M %p, %d %b %Y")

        # create appointment
        apt_id = f"APT{str(self.appointment_counter).zfill(3)}"
        self.appointment_counter += 1
        appointment = Appointment(apt_id, patient, doctor, time_slot)

        # update patient and doctor status
        patient.assigned_doctor = doctor
        patient.appointment_time = time_slot
        patient.status = "assigned"
        doctor.available = False
        doctor.patients_seen += 1

        self.appointments[apt_id] = appointment

        print(f"\n  🏥 Doctor Assigned Successfully!")
        print(f"  {'='*45}")
        print(appointment)
        print(f"  {'='*45}")
        print(f"\n  Dr. {doctor.name} will arrive at your location")
        print(f"  ({patient.location}) by {time_slot}")

        return appointment

    # ── COMPLETE APPOINTMENT ─────────────────────────────────
    def complete_appointment(self, appointment_id):
        """Mark appointment as completed and free the doctor"""
        if appointment_id not in self.appointments:
            print(f"  ❌ Appointment {appointment_id} not found")
            return

        apt = self.appointments[appointment_id]
        apt.status = "completed"
        apt.doctor.available = True   # doctor is free again
        apt.patient.status = "completed"
        print(f"\n  ✅ Appointment {appointment_id} marked as completed")
        print(f"     Dr. {apt.doctor.name} is now available again")

    # ── VIEW ALL PATIENTS ────────────────────────────────────
    def view_all_patients(self):
        """Display all registered patients"""
        if not self.patients:
            print("\n  No patients registered yet.")
            return

        print(f"\n  {'='*55}")
        print(f"  📋 ALL PATIENTS ({len(self.patients)} total)")
        print(f"  {'='*55}")
        for p in self.patients.values():
            status_icon = {"waiting": "⏳", "assigned": "✅", "completed": "🏁"}.get(p.status, "❓")
            print(f"  {status_icon} {p}")
            if p.assigned_doctor:
                print(f"     → Assigned to Dr. {p.assigned_doctor.name} at {p.appointment_time}")

    # ── VIEW ALL DOCTORS ─────────────────────────────────────
    def view_all_doctors(self):
        """Display all registered doctors"""
        print(f"\n  {'='*55}")
        print(f"  👨‍⚕️ ALL DOCTORS ({len(self.doctors)} total)")
        print(f"  {'='*55}")
        for d in self.doctors.values():
            avail_icon = "🟢" if d.available else "🔴"
            print(f"  {avail_icon} {d} | Patients seen: {d.patients_seen}")

    # ── VIEW APPOINTMENTS ────────────────────────────────────
    def view_appointments(self):
        """Display all appointments"""
        if not self.appointments:
            print("\n  No appointments yet.")
            return

        print(f"\n  {'='*55}")
        print(f"  📅 ALL APPOINTMENTS ({len(self.appointments)} total)")
        print(f"  {'='*55}")
        for apt in self.appointments.values():
            print(apt)
            print(f"  {'-'*45}")


# ============================================================
# MAIN — CLI interface
# ============================================================
def main():
    platform = Platform()

    # pre-load doctors
    platform.add_doctor("Sharma",   "General Physician", "Hitech City")
    platform.add_doctor("Rao",      "Cardiologist",      "Banjara Hills")
    platform.add_doctor("Patel",    "Dermatologist",     "Ameerpet")
    platform.add_doctor("Krishnan", "Orthopedist",       "Secunderabad")
    platform.add_doctor("Reddy",    "General Physician", "Uppal")
    platform.add_doctor("Mehta",    "Pediatrician",      "Hitech City")

    print("="*55)
    print("  🏥 DOCTOR-AT-HOME PATIENT PLATFORM")
    print("="*55)
    print("  Bringing healthcare to your doorstep")
    print("="*55)

    while True:
        print("\n  MAIN MENU:")
        print("  1. Register as Patient")
        print("  2. Request Doctor Visit")
        print("  3. View All Patients")
        print("  4. View All Doctors")
        print("  5. View All Appointments")
        print("  6. Complete an Appointment")
        print("  7. Exit")

        choice = input("\n  Enter choice (1-7): ").strip()

        # ── REGISTER PATIENT ──────────────────────────────
        if choice == "1":
            print("\n  --- Patient Registration ---")
            name = input("  Full Name     : ").strip()
            if not name:
                print("  ❌ Name cannot be empty")
                continue

            age_input = input("  Age           : ").strip()
            if not age_input.isdigit():
                print("  ❌ Please enter a valid age")
                continue
            age = int(age_input)

            print("\n  Available locations:")
            locations = ["Hitech City", "Banjara Hills", "Ameerpet",
                         "Secunderabad", "Uppal", "Madhapur"]
            for i, loc in enumerate(locations, 1):
                print(f"    {i}. {loc}")

            loc_input = input("  Choose location (1-6): ").strip()
            if not loc_input.isdigit() or int(loc_input) not in range(1, 7):
                print("  ❌ Invalid location choice")
                continue
            location = locations[int(loc_input) - 1]

            symptoms = input("  Symptoms      : ").strip()
            if not symptoms:
                print("  ❌ Please describe your symptoms")
                continue

            platform.register_patient(name, age, location, symptoms)

        # ── REQUEST DOCTOR ────────────────────────────────
        elif choice == "2":
            print("\n  --- Request Doctor Visit ---")
            patient_id = input("  Enter your Patient ID (e.g. PT001): ").strip()

            if patient_id not in platform.patients:
                print(f"  ❌ Patient ID '{patient_id}' not found")
                print("     Please register first (Option 1)")
                continue

            patient = platform.patients[patient_id]

            if patient.status == "assigned":
                print(f"\n  ⚠️  You already have an appointment!")
                print(f"     Dr. {patient.assigned_doctor.name} "
                      f"at {patient.appointment_time}")
                continue

            print(f"\n  Finding best doctor for {patient.name}...")
            platform.assign_doctor(patient)

        # ── VIEW PATIENTS ─────────────────────────────────
        elif choice == "3":
            platform.view_all_patients()

        # ── VIEW DOCTORS ──────────────────────────────────
        elif choice == "4":
            platform.view_all_doctors()

        # ── VIEW APPOINTMENTS ─────────────────────────────
        elif choice == "5":
            platform.view_appointments()

        # ── COMPLETE APPOINTMENT ──────────────────────────
        elif choice == "6":
            apt_id = input("  Enter Appointment ID (e.g. APT001): ").strip()
            platform.complete_appointment(apt_id)

        # ── EXIT ──────────────────────────────────────────
        elif choice == "7":
            print("\n  Thank you for using Doctor-at-Home! 🏥")
            print("  Stay healthy! 👋")
            break

        else:
            print("  ❌ Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()
