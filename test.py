import datetime
import psutil





process_name = "explorer.exe"
creation_time = get_process_creation_time(process_name=process_name)


if creation_time:
    duration_seconds, duration_minutes, duration_hours = calculate_duration_since_creation(creation_time)
    print(f"The process {process_name} has been running for:")
    print(f"{duration_seconds} seconds")
    print(f"{duration_minutes} minutes")
    print(f"{duration_hours} hours")
else:
    print(f"No process named {process_name} found.")