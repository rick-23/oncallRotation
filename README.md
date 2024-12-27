# Oncall Scheduler Project

Generates weekday and weekend oncall schedule for a team of doctors and algorithm for senior doctors to swap oncalls on thursdays.

The schedule starts from the day the program is executed and schedule can be generated for a configurable amount of time.

### Prerequisites

Before you continue, ensure you have met the following requirements:

- You have installed the latest version of Python based on your Operating System. Download Python from: https://www.python.org/downloads/
- You have pandas installed. To install pandas: pip3 install pandas

### Running this project

To run this project:

- Add/modify the team member names in team_members.csv and senior_team.csv files.
- Open a Command Prompt/Terminal and navigate to the project directory.
- Once the terminal is based in the project directory, run the command: python3 oncall_scheduler.py
- The file oncall_schedule.csv will be generated.
