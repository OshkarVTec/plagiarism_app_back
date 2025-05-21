import os
from plagiarism_algorithms.plagiarism_clusters import plagiarism_detection_clusters
from plagiarism_algorithms.plagiarism_difflib import detect_type_from_files
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException


async def save_files(files, upload_dir: str = "uploaded_files"):
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    else:
        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    file_paths = []
    for file in files:
        filename = file.filename or "unnamed_file"
        file_location = os.path.join(upload_dir, filename)
        content = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        file_paths.append(file_location)


def get_clusters(root_dir: str):
    clustering_results = plagiarism_detection_clusters(root_dir)

    # Detect plagiarism type for every possible pair inside each cluster
    clusters_with_types = {}
    for cluster_id, members in clustering_results.items():
        pairs = []
        # members: {filename: [(start, end), ...], ...}
        files_and_ranges = []
        for filename, intervals in members.items():
            for start, end in intervals:
                files_and_ranges.append((filename, start, end))
        # Generate all unique pairs
        for i in range(len(files_and_ranges)):
            for j in range(i + 1, len(files_and_ranges)):
                file1, start1, end1 = files_and_ranges[i]
                file2, start2, end2 = files_and_ranges[j]
                if file1 == file2:
                    continue  # Skip same file comparisons
                try:
                    clone_type = detect_type_from_files(
                        file1, start1, end1, file2, start2, end2
                    )
                except Exception as e:
                    clone_type = f"Error: {str(e)}"
                pairs.append(
                    {
                        "file1": file1,
                        "lines1": [start1, end1],
                        "file2": file2,
                        "lines2": [start2, end2],
                        "clone_type": clone_type,
                    }
                )
        clusters_with_types[cluster_id] = {"members": members, "pairs": pairs}

    return jsonable_encoder(clusters_with_types)


def get_file_content(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    filename = file_path.split("/")[-1]
    return {"filename": filename, "content": content}
