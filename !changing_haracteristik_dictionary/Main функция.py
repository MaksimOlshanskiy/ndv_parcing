
def main():
    excel_path = r"C:\...\Ноябрь База 7.xlsx"

    df = load_excel(excel_path)

    projects_dict = load_json(r"C:\...\projects.json")
    corpus_dict = load_json(r"C:\...\corpus.json")
    area_dict = load_json(r"C:\...\output.json")

    df = enrich_projects(df, projects_dict)
    df = enrich_corpus(df, corpus_dict)
    df = enrich_area_typology(df, area_dict)

    df.to_excel(excel_path, index=False)
    print("✅ Готово. Файл обработан за один проход.")

if __name__ == "__main__":
    main()