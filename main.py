import json


def main():
    with open("charginStations.json", encoding="utf-8") as f:
        stations = json.load(f)

    locations = []
    chargers = []
    sublocations = []

    for station in stations:
        for key in ("tags", "country", "info", "info_en", "thumb"):
            station.pop(key, None)

        station_chargers = station.pop("chargers", [])
        station_sublocations = station.pop("sublocations", {}) or {}

        for charger in station_chargers:
            operator = charger.pop("operator", {})
            charger["operator_id"] = operator.get("id")
            charger["operator_name"] = operator.get("name")
            for key in ("updated", "info", "info_en", "links", "subtype"):
                charger.pop(key, None)
            chargers.append(charger)

        for subloc in station_sublocations.values():
            subloc["location_title"] = station.get("title")
            for key in ("title_en", "thumb_id", "published_ts"):
                subloc.pop(key, None)
            sublocations.append(subloc)

        locations.append(station)
    
    with open("lk-locations.json", "w", encoding="utf-8") as f:
        json.dump(locations, f, ensure_ascii=False, indent=2)

    with open("lk-chargers.json", "w", encoding="utf-8") as f:
        json.dump(chargers, f, ensure_ascii=False, indent=2)

    with open("lk-sublocations.json", "w", encoding="utf-8") as f:
        json.dump(sublocations, f, ensure_ascii=False, indent=2)

    print(f"Done: {len(locations)} locations, {len(chargers)} chargers, {len(sublocations)} sublocations")


if __name__ == "__main__":
    main()
