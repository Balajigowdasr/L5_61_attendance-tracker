"""Attendance tracker with improved security, reliability, and style."""

import csv
import os
import zipfile
from datetime import datetime

import requests


students = {}
ERP_URL = "https://erp.college.example/api/attendance"
MIN_ATTENDANCE = 75


def add_student(roll_no, name, section="A"):
    """Add a student to the attendance register."""
    students[roll_no] = {
        "name": name,
        "section": section,
        "records": [],
    }


def mark_attendance(roll_no, date, status, register=None):
    """Record attendance and return the daily register."""
    if register is None:
        register = {}

    register.setdefault(date, []).append(roll_no)
    students[roll_no]["records"].append((date, status))
    return register


def attendance_percentage(roll_no):
    """Calculate a student's attendance percentage."""
    records = students[roll_no]["records"]
    if not records:
        return 0

    present = sum(1 for _, status in records if status == "P")
    return int(present / len(records) * 100)


def is_eligible(percentage):
    """Check whether attendance meets the minimum requirement."""
    return percentage >= MIN_ATTENDANCE


def shortage_list():
    """Return students below the minimum attendance requirement."""
    result = [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]
    return result or None


def has_long_absence(roll_no, days=3):
    """Check for consecutive absences."""
    if days <= 0:
        return False

    statuses = [
        status for _, status in students[roll_no]["records"]
    ]
    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(len(statuses) - days + 1)
    )


def latest_date(roll_no):
    """Return the latest attendance date, or None if no records exist."""
    dates = [
        date for date, _ in students[roll_no]["records"]
    ]
    if not dates:
        return None

    return max(
        dates,
        key=lambda date: datetime.strptime(date, "%Y-%m-%d"),
    )


def safe_csv_value(value):
    """Prevent spreadsheet formula execution in exported text values."""
    if isinstance(value, str) and value.startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def export_csv(path="attendance.csv"):
    """Export attendance percentages to a UTF-8 CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["roll_no", "name", "percentage"])

        for roll_no, student in students.items():
            writer.writerow(
                [
                    safe_csv_value(roll_no),
                    safe_csv_value(student["name"]),
                    attendance_percentage(roll_no),
                ]
            )

    return path


def sync_to_erp(roll_no):
    """Send attendance to the ERP service using a configured API key."""
    api_key = os.environ.get("ERP_API_KEY")
    if not api_key:
        raise RuntimeError("Set the ERP_API_KEY environment variable.")

    payload = {
        "roll_no": roll_no,
        "pct": attendance_percentage(roll_no),
    }
    response = requests.post(
        ERP_URL,
        json=payload,
        headers={"X-API-Key": api_key},
        timeout=10,
    )
    response.raise_for_status()
    return response.status_code


def backup_reports():
    """Create a ZIP backup of CSV reports in the current directory."""
    archive_name = "reports_backup.zip"
    current_directory = os.path.abspath(".")

    with zipfile.ZipFile(
        archive_name, "w", zipfile.ZIP_DEFLATED
    ) as archive:
        for filename in os.listdir(current_directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(current_directory, filename)
                archive.write(file_path, arcname=filename)

    return archive_name


def run_job(command):
    """Describe a command without invoking a system shell."""
    if not isinstance(command, list) or not command:
        raise ValueError("Command must be a non-empty list of arguments.")

    return {"command": command, "shell": False}


def schedule_reminders():
    """Prepare a reminder command without executing it."""
    return run_job(["send_sms", "--shortage"])


def main():
    """Run the attendance tracker demonstration."""
    add_student("R01", "Aditi")
    add_student("R02", '=HYPERLINK("http://evil.example","Bharat")')

    register = {}

    first_records = [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]
    for date, status in first_records:
        mark_attendance("R01", date, status, register)

    second_records = [
        ("2026-09-01", "P"),
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-09-03", "P"),
    ]
    for date, status in second_records:
        mark_attendance("R02", date, status, register)

    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print("Register entries for 2026-09-01:", register["2026-09-01"])
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (no network)")


if __name__ == "__main__":
    main()
