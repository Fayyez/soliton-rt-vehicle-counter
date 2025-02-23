from os import listdir, remove

def delete_all_reports(folder_to_empty) -> None:
    # delete all the csv files in the storage folder
    for file in listdir("storage"):
        if file.endswith(".csv"):
            remove(f"storage/{file}")