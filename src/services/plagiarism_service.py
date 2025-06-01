from plagiarism_algorithms.plagiarism_clusters import plagiarism_detection_clusters
from plagiarism_algorithms.plagiarism_difflib import detect_type_from_files
from fastapi.encoders import jsonable_encoder
import os

def get_clusters(root_dir: str):
    clustering_results = plagiarism_detection_clusters(root_dir)
    clusters_with_pairs = {}

    for cluster_id, members in clustering_results.items():
        files = list(members.keys())
        pairs = []
        # Comparar todos los archivos entre sí (uno contra uno)
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                file1 = files[i]
                file2 = files[j]
                # Comparar archivos completos: líneas 1 hasta EOF
                with open(file1, "r", encoding="utf-8") as f1:
                    lines1 = f1.readlines()
                with open(file2, "r", encoding="utf-8") as f2:
                    lines2 = f2.readlines()
                start1, end1 = 1, len(lines1)
                start2, end2 = 1, len(lines2)
                clone_type = detect_type_from_files(
                    file1, start1, end1, file2, start2, end2
                )
                pairs.append(
                    {
                        "file1": file1,
                        "file2": file2,
                        "clone_type": clone_type,
                    }
                )
        clusters_with_pairs[cluster_id] = {"members": members, "file_pairs": pairs}

    return jsonable_encoder(clusters_with_pairs)

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