
def get_file_content(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    filename = file_path.split("/")[-1]
    return {"filename": filename, "content": content}
