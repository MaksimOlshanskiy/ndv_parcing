import json

with open(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!changing_haracteristik_dictionary\projects.json", "r", encoding="utf-8") as f:
    data = json.load(f)

unique_ids = list({
    v["ID дом.рф"]
    for project in data.values()
    for v in project.values()
    if (
        isinstance(v, dict)
        and "ID дом.рф" in v
        and v.get("Стадия строительной готовности") != "введен"
    )
})

print(unique_ids)