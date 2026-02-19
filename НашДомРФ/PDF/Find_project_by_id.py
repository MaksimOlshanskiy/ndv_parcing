import json

def find_project_and_building(data, target_domrf_id):
    """
    data — весь JSON (как dict)
    target_domrf_id — ID дом.рф (int или str)
    """

    target_domrf_id = str(target_domrf_id)

    for project_name, buildings in data.items():
        for building_number, building_data in buildings.items():

            if str(building_data.get("ID дом.рф")) == target_domrf_id:

                return {
                    "project_name": project_name,
                    "building_number": building_number
                }
    return {
        "project_name": '',
        "building_number": ''
    }



