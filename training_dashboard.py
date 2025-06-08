import argparse

# Dummy Data for CLI Demo
fresher_data = {
    "Venkat": {
        "daily_quiz": "Completed",
        "coding_challenge": "In Progress",
        "assignment": "Submitted",
        "certification": "In Progress",
        "workflow": {
            "profile_updated": True,
            "daily_quiz_completed": True,
            "coding_challenge_submitted": False,
            "assignment_submitted": True,
            "certification_completed": False
        },
        "skill": "Python",
        "department": "Data Engineering"
    }
}

def fresher_status(name):
    user = fresher_data.get(name)
    if not user:
        print(f"No data found for {name}")
        return
    print(f"\n--- Training Status for {name} ---")
    print(f"Daily Quiz Status: {user['daily_quiz']}")
    print(f"Coding Challenge Progress: {user['coding_challenge']}")
    print(f"Assignment Submission: {user['assignment']}")
    print(f"Certification Completion: {user['certification']}")
    print("Real-Time Workflow Progress:")
    for k, v in user['workflow'].items():
        print(f"  - {k.replace('_', ' ').title()}: {'✓' if v else '✗'}")
    print("-------------------------------------\n")

def admin_report(department=None):
    print(f"\n--- Admin Console Report ({department if department else 'All'}) ---")
    for name, data in fresher_data.items():
        if department and data["department"] != department:
            continue
        print(f"{name}:")
        print(f"  Skill: {data['skill']}")
        print(f"  Department: {data['department']}")
        print(f"  Status - Quiz: {data['daily_quiz']}, Coding: {data['coding_challenge']}, "
              f"Assignment: {data['assignment']}, Cert: {data['certification']}")
    print("-------------------------------------------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Training Progress CLI")

    subparsers = parser.add_subparsers(dest="command")

    fresher_parser = subparsers.add_parser("fresher-status", help="Check training status for a fresher")
    fresher_parser.add_argument("--name", required=True, help="Name of the fresher")

    admin_parser = subparsers.add_parser("admin-report", help="Generate admin training report")
    admin_parser.add_argument("--department", help="Department filter")

    args = parser.parse_args()

    if args.command == "fresher-status":
        fresher_status(args.name)
    elif args.command == "admin-report":
        admin_report(args.department)
    else:
        parser.print_help()