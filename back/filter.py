import json
from datetime import datetime

def filter_json_by_location_day_and_time(location_keyword='', day_of_week='', input_time=''):
    input_file_path = 'data_exact.json'
    output_file_path = 'filtered_data_exact.json'
    """
    Filters the JSON data from the input file based on a location keyword, day of the week, and a specific time.
    Writes the filtered data to a new file.

    Args:
        location_keyword (str): A single location keyword to filter on.
        day_of_week (str): The day of the week to filter on.
        input_time (str): The time to filter on (HH:MM format).
    """
    
    def contains_location_keyword(obj, keyword):
        """
        Recursively checks if the keyword exists in any of the object's values.
        """
        if isinstance(obj, dict):
            return any(contains_location_keyword(v, keyword) for v in obj.values())
        elif isinstance(obj, list):
            return any(contains_location_keyword(v, keyword) for v in obj)
        elif isinstance(obj, str):
            return keyword.lower() in obj.lower()
        else:
            return False
    
    def is_open_on_day(entry, day):
        """
        Checks if the business is open on the specified day of the week.
        """
        if day == '':  # If day filter is empty, skip it (all entries pass)
            return True
        opening_times = entry.get('Opening Times', {})
        day_status = opening_times.get(day, 'Closed')
        return day_status.lower() != 'closed'
    
    def is_open_at_time(entry, day, input_time):
        """
        Checks if the business is open at the specified time on the given day.
        If day is empty, it checks for the time across **all days**.
        """
        if input_time == '':  # If time filter is empty, skip it (all entries pass)
            return True
        
        opening_times = entry.get('Opening Times', {})
        
        if day == '':  # If no specific day is given, check all days in "Opening Times"
            days_to_check = opening_times.keys()
        else:
            days_to_check = [day]

        # Convert input time to datetime for comparison
        input_time_obj = datetime.strptime(input_time, "%H:%M")
        
        for current_day in days_to_check:
            day_schedule = opening_times.get(current_day, 'Closed')
            
            if day_schedule.lower() == 'closed':
                continue
            
            # Parse the time ranges for the day (e.g., "8:30 - 12:00 / 13:30 - 18:30")
            time_ranges = [time_range.strip() for time_range in day_schedule.split('/')]
            
            for time_range in time_ranges:
                try:
                    start_time, end_time = [t.strip() for t in time_range.split('-')]
                    start_time_obj = datetime.strptime(start_time, "%H:%M")
                    end_time_obj = datetime.strptime(end_time, "%H:%M")
                    
                    if start_time_obj <= input_time_obj <= end_time_obj:
                        return True  # If the input time is within the current range, return True
                except ValueError as e:
                    continue
        
        return False
    
    # Load data from the input file
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Filter data based on location, day of the week, and time
    filtered_data = [
        entry for entry in data 
        if (location_keyword == '' or contains_location_keyword(entry, location_keyword)) 
        and (day_of_week == '' or is_open_on_day(entry, day_of_week)) 
        and (input_time == '' or is_open_at_time(entry, day_of_week, input_time))
    ]
    
    # Write filtered data to the output file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

# Example usage
# filter_json_by_location_day_and_time('', '', '')  # Filter only by time (works now)
# filter_json_by_location_day_and_time('Lugano', '', '10:00')  # Filter by location and time
# filter_json_by_location_day_and_time('', 'Sunday', '22:00')  # Filter by day and time
# filter_json_by_location_day_and_time('', 'Sunday', '')  # Filter only by day
# filter_json_by_location_day_and_time('Lugano', '', '')  # Filter only by location
# filter_json_by_location_day_and_time('Lugano', 'Sunday', '')  # Filter by location and day
# filter_json_by_location_day_and_time('Lugano', 'Sunday', '10:00')  # Filter by location, day, and time
