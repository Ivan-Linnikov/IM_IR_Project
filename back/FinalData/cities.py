import json
import re


def extract_unique_cities(input_file_path: str, output_file_path: str) -> None:
    """
    Reads a JSON file, extracts unique cities from the 'Address' field, 
    and writes them into a new JSON file.

    Args:
        input_file_path (str): Path to the input JSON file.
        output_file_path (str): Path to the output JSON file with unique cities.
    """
    
    # List to store unique cities
    unique_cities = set()
    
    # Regex pattern to extract city after 4-digit zip code
    city_pattern = re.compile(r"\b\d{4}\s+([A-Za-z\-\s]+)")
    
    try:
        # Read the input JSON file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            # Extract city from the 'Address' field of each record
            for record in data:
                address = record.get("Address", "")
                match = city_pattern.search(address)
                if match:
                    city = match.group(1).strip()
                    unique_cities.add(city)
            
        # Convert the set of unique cities into a sorted list
        unique_cities_list = sorted(unique_cities)
        
        # Write the unique cities to an output JSON file
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(unique_cities_list, output_file, ensure_ascii=False, indent=4)
        
        print(f"Successfully extracted and saved {len(unique_cities_list)} unique cities to {output_file_path}.")
        
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
extract_unique_cities('back/FinalData/FinalLocal.json', 'back/FinalData/uniquecities.json')