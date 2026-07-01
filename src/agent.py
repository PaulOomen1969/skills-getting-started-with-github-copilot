from typing import Dict, List
from src.app import activities


def list_activities() -> List[Dict[str, str]]:
    return [
        {
            "name": name,
            "description": activity["description"],
            "schedule": activity["schedule"],
            "participants": len(activity["participants"]),
            "max_participants": activity["max_participants"],
        }
        for name, activity in activities.items()
    ]


def find_duplicate_signups() -> Dict[str, List[str]]:
    duplicates = {}
    for name, activity in activities.items():
        seen = set()
        dupes = []
        for email in activity["participants"]:
            if email in seen and email not in dupes:
                dupes.append(email)
            seen.add(email)
        if dupes:
            duplicates[name] = dupes
    return duplicates


def validate_signup(activity_name: str, email: str) -> str:
    if activity_name not in activities:
        return f"Activity '{activity_name}' does not exist."

    activity = activities[activity_name]
    if email in activity["participants"]:
        return f"{email} is already signed up for {activity_name}."

    if len(activity["participants"]) >= activity["max_participants"]:
        return f"{activity_name} is full ({activity['max_participants']} participants)."

    return f"{email} can sign up for {activity_name}."


def describe_signup_bug() -> str:
    return (
        "The current signup endpoint adds every submitted email to the activity participants list "
        "without checking for duplicates or maximum capacity. This allows the same student to "
        "register more than once and does not enforce the activity limit."
    )


def summary() -> str:
    lines = ["Mergington High School Copilot Agent Summary:\n"]
    for info in list_activities():
        lines.append(
            f"- {info['name']}: {info['participants']}/{info['max_participants']} participants; "
            f"{info['schedule']}"
        )
    duplicates = find_duplicate_signups()
    if duplicates:
        lines.append("\nDuplicate signups detected:")
        for name, dupes in duplicates.items():
            lines.append(f"- {name}: {', '.join(dupes)}")
    else:
        lines.append("\nNo duplicate signups found.")
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Local agent helper for the Mergington High School signup app."
    )
    parser.add_argument(
        "command",
        choices=["status", "duplicates", "validate", "bug", "summary"],
        help="Command to run",
    )
    parser.add_argument("--activity", help="Activity name for validation")
    parser.add_argument("--email", help="Student email for validation")
    args = parser.parse_args()

    if args.command == "status":
        for activity in list_activities():
            print(
                f"{activity['name']}: {activity['participants']}/{activity['max_participants']} participants "
                f"({activity['schedule']})"
            )
    elif args.command == "duplicates":
        duplicates = find_duplicate_signups()
        if not duplicates:
            print("No duplicate signups found.")
        else:
            for name, dupes in duplicates.items():
                print(f"{name}: {', '.join(dupes)}")
    elif args.command == "validate":
        if not args.activity or not args.email:
            parser.error("--activity and --email are required for validate")
        print(validate_signup(args.activity, args.email))
    elif args.command == "bug":
        print(describe_signup_bug())
    elif args.command == "summary":
        print(summary())
