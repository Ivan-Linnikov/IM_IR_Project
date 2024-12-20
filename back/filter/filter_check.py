# Import the filter function from filter_json_data
from filter import filter_json_by_location_day_and_time

# Call the function with the paths and location keywords
filter_json_by_location_day_and_time('Lugano', 'Tuesday', '9:30')

print("Filtering complete. Filtered data written to filtered_data_ex.json.")