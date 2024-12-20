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
        if day == '':  
            return True
        opening_times = entry.get('Opening Times', {})
        day_status = opening_times.get(day, 'Closed')
        return day_status.lower() != 'closed'
    
    def is_open_at_time(entry, day, input_time):
        """
        Checks if the business is open at the specified time on the given day.
        If day is empty, it checks for the time across **all days**.
        """
        if input_time == '':  
            return True
        
        opening_times = entry.get('Opening Times', {})
        
        if day == '': 
            days_to_check = opening_times.keys()
        else:
            days_to_check = [day]

        input_time_obj = datetime.strptime(input_time, "%H:%M")
        
        for current_day in days_to_check:
            day_schedule = opening_times.get(current_day, 'Closed')
            
            if day_schedule.lower() == 'closed':
                continue
            
            time_ranges = [time_range.strip() for time_range in day_schedule.split('/')]
            
            for time_range in time_ranges:
                try:
                    start_time, end_time = [t.strip() for t in time_range.split('-')]
                    start_time_obj = datetime.strptime(start_time, "%H:%M")
                    end_time_obj = datetime.strptime(end_time, "%H:%M")
                    
                    if start_time_obj <= input_time_obj <= end_time_obj:
                        return True  
                except ValueError as e:
                    continue
        
        return False
    
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    filtered_data = [
        entry for entry in data 
        if (location_keyword == '' or contains_location_keyword(entry, location_keyword)) 
        and (day_of_week == '' or is_open_on_day(entry, day_of_week)) 
        and (input_time == '' or is_open_at_time(entry, day_of_week, input_time))
    ]
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

