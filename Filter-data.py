import os
import json

COUNT = {}

def check_null(value, label):
    if value is None:
        if str(label) in COUNT:
            COUNT[str(label)] += 1
        else:
            COUNT[str(label)] = 0
        return False
    else:
        return True

def check_list(attribute, label):
    if attribute is None:
        if str(label) in COUNT:
            COUNT[str(label)] += 1
        else:
            COUNT[str(label)] = 0
        return False
    elif len(attribute) == 0:
        if str(label) in COUNT:
            COUNT[str(label)] += 1
        else:
            COUNT[str(label)] = 0
        return False
    else:
        return True

def check(data):

    main_country_code = data.get("main_country_code")
    main_latitude = data.get("main_latitude")
    main_longitude = data.get("main_longitude")
    num_locations = data.get("num_locations")
    company_type = data.get("company_type")
    year_founded = data.get("year_founded")
    employee_count = data.get("employee_count")
    estimated_revenue = data.get("estimated_revenue")
    long_description = data.get("long_description")
    business_tags = data.get("business_tags")
    main_business_category = data.get("main_business_category")
    main_industry = data.get("main_industry")
    alexa_rank = data.get("alexa_rank")
    technologies = data.get("technologies")
    naics_2022 = data.get("naics_2022", {})
    if naics_2022 is not None:
        naics_2022_primary=naics_2022.get("primary")
    else:
        naics_2022_primary = None

    nace_rev2 = data.get("nace_rev2")
    ncci_codes_28_1 = data.get("ncci_codes_28_1")
    sic = data.get("sic")
    isic_v4 = data.get("isic_v4")
    ibc_insurance = data.get("ibc_insurance")
        
    # Check conditions
    results = [
        check_null(main_country_code, "main_country_code"),
        check_null(main_latitude, "main_latitude"),
        check_null(main_longitude, "main_longitude"),
        check_null(num_locations, "num_locations"),
        check_null(company_type, "company_type"),
        check_null(year_founded, "year_founded"),
        check_null(employee_count, "employee_count"),
        check_null(estimated_revenue, "estimated_revenue"),
        check_null(long_description, "long_description"),
        check_list(business_tags, "business_tags"),
        check_null(main_business_category, "main_business_category"),
        check_null(main_industry, "main_industry"),
        # check_null(alexa_rank, "alexa_rank"),
        check_list(technologies, "technologies"),
        check_null(naics_2022_primary, "naics_2022_primary"),
        check_list(nace_rev2, "nace_rev2"),
        check_list(ncci_codes_28_1, "ncci_codes_28_1"),
        check_list(sic, "sic"),
        check_list(isic_v4, "isic_v4"),
        check_list(ibc_insurance, "ibc_insurance"),
    ]
    if False in results:
        return False
    else:
        return True
    
file_path = os.path.join("EDA", "search_100k.jsonl")

with open(file_path, "r") as json_file:
    files = json.load(json_file)

new_files = []
for file in files:
    if check(file):
        new_files.append(file)
print(COUNT)
print(len(new_files))
file_path = os.path.join("EDA", "search_100k_no_none.jsonl")
with open(file_path, "w") as json_file:
    json.dump(new_files, json_file, indent=4)