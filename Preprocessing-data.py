import json
from sklearn.preprocessing import LabelEncoder
import joblib
from statistics import mean, stdev

file_path = 'raw_data.json'

with open(file_path, 'r') as file:
    data = json.load(file)


# Extract the values of the categorical features for label encoding
main_country_codes = [entry['main_country_code'] for entry in data]
company_types = [entry['company_type'] for entry in data]
main_industries = [entry['main_industry'] for entry in data]

# Initialize label encoders
main_country_code_encoder = LabelEncoder()
company_type_encoder = LabelEncoder()
main_industry_encoder = LabelEncoder()

# Fit and transform the label encoders
main_country_codes_encoded = main_country_code_encoder.fit_transform(main_country_codes)
company_types_encoded = company_type_encoder.fit_transform(company_types)
main_industries_encoded = main_industry_encoder.fit_transform(main_industries)

# Save the label encoders to disk
path = "encoders/"
joblib.dump(main_country_code_encoder, path+'main_country_code_encoder.joblib')
joblib.dump(company_type_encoder, path+'company_type_encoder.joblib')
joblib.dump(main_industry_encoder, path+'main_industry_encoder.joblib')

# Initialize a dictionary to store the extracted data
extracted_data = []

# Iterate over each entry in the JSON data
for entry in data:
    # Process 'nace_rev2'
    nace_rev2_values = entry['nace_rev2']
    nace_rev2_codes = [float(item['code']) for item in nace_rev2_values]
    nace_rev2_len = int(len(nace_rev2_values))
    nace_rev2_mean = float(mean(nace_rev2_codes))
    nace_rev2_min = float(min(nace_rev2_codes))
    nace_rev2_max = float(max(nace_rev2_codes))
    nace_rev2_std = float(stdev(nace_rev2_codes) if nace_rev2_len >= 2 else 0)

    # Process 'ncci_codes_28_1'
    ncci_codes_values = entry['ncci_codes_28_1']
    ncci_codes_codes = [int(code) for code in ncci_codes_values]
    ncci_codes_len = int(len(ncci_codes_values))
    ncci_codes_mean = float(mean(ncci_codes_codes))
    ncci_codes_min = int(min(ncci_codes_codes))
    ncci_codes_max = int(max(ncci_codes_codes))
    ncci_codes_std = float(stdev(ncci_codes_codes) if ncci_codes_len >= 2 else 0)

    # Process 'sic'
    sic_values = entry['sic']
    sic_codes = [int(item['code']) for item in sic_values]
    sic_len = int(len(sic_values))
    sic_mean = float(mean(sic_codes))
    sic_min = int(min(sic_codes))
    sic_max = int(max(sic_codes))
    sic_std = float(stdev(sic_codes) if sic_len >= 2 else 0)

    # Process 'isic_v4'
    isic_v4_values = entry['isic_v4']
    isic_v4_codes = [int(item['code']) for item in isic_v4_values]
    isic_v4_len = int(len(isic_v4_values))
    isic_v4_mean = float(mean(isic_v4_codes))
    isic_v4_min = int(min(isic_v4_codes))
    isic_v4_max = int(max(isic_v4_codes))
    isic_v4_std = float(stdev(isic_v4_codes) if isic_v4_len >= 2 else 0)

    # Process 'ibc_insurance'
    ibc_insurance_values = entry['ibc_insurance']
    ibc_insurance_codes = [int(item['code']) for item in ibc_insurance_values]
    ibc_insurance_len = int(len(ibc_insurance_values))
    ibc_insurance_mean = float(mean(ibc_insurance_codes))
    ibc_insurance_min = int(min(ibc_insurance_codes))
    ibc_insurance_max = int(max(ibc_insurance_codes))
    ibc_insurance_std = float(stdev(ibc_insurance_codes) if ibc_insurance_len >= 2 else 0)

    extracted_entry = {
        'soleadify_id': entry["soleadify_id"],
        'main_country_code': int(main_country_code_encoder.transform([entry['main_country_code']])[0]),
        'main_latitude': float(entry["main_latitude"]),
        'main_longitude': float(entry["main_longitude"]),
        'num_locations': int(entry["num_locations"]),
        'company_type': int(company_type_encoder.transform([entry['company_type']])[0]),
        'year_founded': int(entry["year_founded"]),
        'employee_count': int(entry["employee_count"]),
        'estimated_revenue': int(entry["estimated_revenue"]),
        'long_description': float(entry['long_description']),
        'business_tags': float(entry['business_tags']),
        'main_business_category': float(entry['main_business_category']),
        'technologies': float(entry['technologies']),
        'naics_2022': int(entry['naics_2022']['primary']["code"]),
        'nace_rev2': {
            'len': nace_rev2_len,
            'mean': nace_rev2_mean,
            'min': nace_rev2_min,
            'max': nace_rev2_max,
            "std": nace_rev2_std
        },
        'ncci_codes_28_1': {
            'len': ncci_codes_len,
            'mean': ncci_codes_mean,
            'min': ncci_codes_min,
            'max': ncci_codes_max,
            "std": ncci_codes_std
        },
        'sic': {
            'len': sic_len,
            'mean': sic_mean,
            'min': sic_min,
            'max': sic_max,
            "std": sic_std
        },
        'isic_v4': {
            'len': isic_v4_len,
            'mean': isic_v4_mean,
            'min': isic_v4_min,
            'max': isic_v4_max,
            "std": isic_v4_std
        },
        'ibc_insurance': {
            'len': ibc_insurance_len,
            'mean': ibc_insurance_mean,
            'min': ibc_insurance_min,
            'max': ibc_insurance_max,
            "std": ibc_insurance_std
        },
    }
    extracted_data.append(extracted_entry)


# Initialize dictionaries to store minimum and maximum values for each field
min_values = {}
max_values = {}


# Iterate through each company
for company in extracted_data:
    # Create a copy of the keys to iterate over
    keys_to_remove = list(company.keys())

    # Iterate through each key in the company dictionary
    for key in keys_to_remove:
        value = company[key]
        if isinstance(value, dict) and key != "naics_2022":
            # Extract values and create new keys
            new_keys = [f"{key}_{sub_key}" for sub_key in value.keys()]
            new_values = list(value.values())

            # Create a dictionary with the new keys and values
            new_dict = dict(zip(new_keys, new_values))

            # Update the company dictionary
            company.update(new_dict)

            # Remove the old key
            del company[key]


# Iterate through each entry in the extracted_data
for entry in extracted_data:
    for key, value in entry.items():
        if key != "soleadify_id":
            # Update minimum and maximum values for non-nested fields
            min_values.setdefault(key, float('inf'))
            max_values.setdefault(key, float('-inf'))
            min_values[key] = min(min_values[key], value)
            max_values[key] = max(max_values[key], value)

# Print or use the min_values and max_values dictionaries as needed
print("Global Minimum Values:")
print(min_values)

print("\nGlobal Maximum Values:")
print(max_values)

def save_as_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file)


with open('parsed_all_V2.json', 'w') as output_file:
    json.dump(extracted_data, output_file, indent=2)
with open('min_values_V2.json', 'w') as output_file:
    json.dump(min_values, output_file, indent=2)
with open('max_values_V2.json', 'w') as output_file:
    json.dump(max_values, output_file, indent=2)



unique_main_country_codes = set()
unique_main_latitudes = set()
unique_main_longitudes = set()
unique_num_locations = set()
unique_company_types = set()
unique_year_founded = set()
unique_employee_counts = set()
unique_estimated_revenues = set()
unique_long_descriptions = set()
unique_business_tags = set()
unique_main_business_categories = set()
unique_technologies = set()
unique_naics_2022 = set()

# Assuming `data` is your list of entries
for entry in data:
    unique_main_country_codes.add(entry['main_country_code'])
    # unique_main_latitudes.add(float(entry["main_latitude"]))
    # unique_main_longitudes.add(float(entry["main_longitude"]))
    unique_num_locations.add(int(entry["num_locations"]))
    unique_company_types.add(entry['company_type'])
    unique_year_founded.add(int(entry["year_founded"]))
    unique_employee_counts.add(int(entry["employee_count"]))
    unique_estimated_revenues.add(int(entry["estimated_revenue"]))
    # unique_long_descriptions.add(float(entry['long_description']))
    # unique_business_tags.add(float(entry['business_tags']))
    # unique_main_business_categories.add(float(entry['main_business_category']))
    # unique_technologies.add(float(entry['technologies']))
    unique_naics_2022.add(int(entry['naics_2022']['primary']["code"]))

# Convert sets to lists if needed
unique_main_country_codes = list(unique_main_country_codes)
# unique_main_latitudes = list(unique_main_latitudes)
# unique_main_longitudes = list(unique_main_longitudes)
unique_num_locations = list(unique_num_locations)
unique_company_types = list(unique_company_types)
unique_year_founded = list(unique_year_founded)
unique_employee_counts = list(unique_employee_counts)
unique_estimated_revenues = list(unique_estimated_revenues)
# unique_long_descriptions = list(unique_long_descriptions)
# unique_business_tags = list(unique_business_tags)
# unique_main_business_categories = list(unique_main_business_categories)
# unique_technologies = list(unique_technologies)
unique_naics_2022 = list(unique_naics_2022)



save_as_json('main_country_codes.json', unique_main_country_codes)
# save_as_json('main_latitudes.json', unique_main_latitudes)
# save_as_json('main_longitudes.json', unique_main_longitudes)
save_as_json('num_locations.json', unique_num_locations)
save_as_json('company_types.json', unique_company_types)
save_as_json('year_founded.json', unique_year_founded)
save_as_json('employee_counts.json', unique_employee_counts)
save_as_json('estimated_revenues.json', unique_estimated_revenues)
# save_as_json('long_descriptions.json', unique_long_descriptions)
# save_as_json('business_tags.json', unique_business_tags)
# save_as_json('main_business_categories.json', unique_main_business_categories)
# save_as_json('technologies.json', unique_technologies)
save_as_json('naics_2022.json', unique_naics_2022)