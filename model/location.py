from model.company import Company


def get_locations() -> {}:
    output = {}
    companies = Company.get_companies()

    for comp in companies["companies"]:
        try:
            locs = comp["locations"]
        except:
            continue

        for loc in locs:
            location_key = comp["name"] + " - " + loc
            output[location_key] = location_key

    return output
