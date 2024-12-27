import pandas as pd
from datetime import datetime, timedelta

class OnCallScheduler:
    def __init__(self, doctors, senior_doctors, start_date=None):
        # Initialize the doctors list and senior doctors list
        self.doctors = doctors
        self.senior_doctors = senior_doctors
        self.start_date = start_date or datetime.today()
        self.weekday_queue = doctors.copy()  # Copy to use for weekday rotation
        self.weekend_queue = doctors.copy()  # Copy to use for weekend rotation
    
    def get_next_oncall(self, queue):
        """ Get the next on-call person from the given queue (round robin) """
        next_oncall = queue.pop(0)
        queue.append(next_oncall)  # Rotate the queue
        return next_oncall
    
    def generate_schedule(self, num_days=7):
        """ Generate an on-call schedule for a given number of days """
        schedule = []
        current_date = self.start_date
        
        for _ in range(num_days):
            day_of_week = current_date.weekday()  # Monday=0, Sunday=6
            
            if day_of_week < 5:  # Weekday (Monday - Friday)
                oncall = self.get_next_oncall(self.weekday_queue)
                if day_of_week == 3:  # Thursday check for senior doctors
                    if oncall in self.senior_doctors:
                        # If a senior engineer is oncall on Thursday, swap with next day's oncall
                        self._swap_thursday_oncall(oncall)
                        oncall = self.get_next_oncall(self.weekday_queue)
            
            else:  # Weekend (Saturday and Sunday)
                oncall = self.get_next_oncall(self.weekend_queue)
            
            schedule.append((current_date.strftime('%Y-%m-%d'), oncall))
            current_date += timedelta(days=1)
        
        return schedule

    def _swap_thursday_oncall(self, current_oncall):
        """ Swap the Thursday oncall with the next day (Friday) if necessary """
        friday_oncall = self.weekday_queue[0]   # Friday's oncall is the second in the queue
        # If Thursday's on-call doctors is a senior doctors, swap them
        if current_oncall in self.senior_doctors:
            # Swap Thursday with Friday directly in the queue
            self.weekday_queue[0], self.weekday_queue[1] = friday_oncall, current_oncall


def load_doctors_from_csv(doctors_file, seniors_file):
    """ Load doctors and senior doctors from CSV files """
    doctors_df = pd.read_csv(doctors_file)
    senior_doctors_df = pd.read_csv(seniors_file)
    
    doctors = doctors_df['doctor'].tolist()
    senior_doctors = senior_doctors_df['doctor'].tolist()
    
    return doctors, senior_doctors

def export_schedule_to_csv(schedule, output_file):
    """ Export the schedule to a CSV file """
    df = pd.DataFrame(schedule, columns=['date', 'oncall'])
    df.to_csv(output_file, index=False)

# Example usage:
if __name__ == "__main__":
    # Load Doctors and senior doctors from CSV files
    doctors, senior_doctors = load_doctors_from_csv('team_members.csv', 'senior_team.csv')
    
    # Create the scheduler
    scheduler = OnCallScheduler(doctors, senior_doctors)
    
    # Generate the schedule for 365 days
    schedule = scheduler.generate_schedule(num_days=365)
    
    # Export the schedule to a CSV file
    export_schedule_to_csv(schedule, 'oncall_schedule.csv')
    
    # Optional: print the schedule for the first few days
    for date, oncall in schedule[:10]:  # Print first 10 days
        print(f"{date}: {oncall}")
