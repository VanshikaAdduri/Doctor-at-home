# Doctor-at-Home Patient Platform 🏥

A CLI-based platform where patients register and a doctor is automatically assigned and dispatched to their location for a home visit.

## 📖 What it does
- Patients register with name, age, location, and symptoms
- System maintains a registry of doctors with specializations and locations
- Priority-based assignment algorithm finds the best available doctor
- Appointment is created with a time slot and confirmation
- Doctor is marked busy during visit and freed after completion
- Full appointment lifecycle: registered → assigned → completed

## 💡 Assignment Algorithm Priority
```
Priority 1 → Same location + matching specialization  (best match)
Priority 2 → Same location, any specialization
Priority 3 → Matching specialization, any location
Priority 4 → Any available doctor                     (last resort)
```

## 🛠️ Tech Stack
- Language: Python
- Concepts: OOP (4 classes), Dictionary, CLI, Priority Logic

## 📦 Class Design
| Class | Represents | Key Attributes |
|---|---|---|
| Patient | Person needing care | name, age, location, symptoms, status |
| Doctor | Medical professional | name, specialization, location, available |
| Appointment | Confirmed booking | patient, doctor, time_slot, status |
| Platform | The entire system | patients{}, doctors{}, appointments{} |

## 🏃 How to Run
```bash
python doctor_at_home.py
```

## 📋 Menu Options
```
1. Register as Patient
2. Request Doctor Visit
3. View All Patients
4. View All Doctors
5. View All Appointments
6. Complete an Appointment
7. Exit
```

## 📊 Sample Interaction
```
Enter Full Name     : Vanshika
Enter Age           : 21
Choose location     : 1 (Hitech City)
Enter Symptoms      : fever and cough

✅ Patient registered! ID: PT001

Finding best doctor for Vanshika...

🏥 Doctor Assigned!
Patient  : Vanshika (Hitech City)
Doctor   : Dr. Sharma (General Physician)
Time     : 03:30 PM, 25 Jun 2026
Status   : Confirmed
```

## 🔧 How to Customise
- Add more doctors in `main()` with different specializations
- Add more symptom keywords to the `symptom_map` dictionary
- Extend to add prescription tracking or payment logic

