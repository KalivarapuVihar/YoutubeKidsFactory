from utils.file_manager import FileManager

lesson = {
    "topic": "Banana",
    "language": "English"
}

FileManager.save_json(
    "output/lessons/banana.json",
    lesson
)

loaded = FileManager.read_json(
    "output/lessons/banana.json"
)

print(loaded)

FileManager.save_text(
    "output/Notes.txt",
    "Hello from FileManager to Notes!"
)

print(
    FileManager.read_text(
        "output/Notes.txt"
    )
)

print(
    FileManager.file_exists(
        "output/Notes.txt"
    )
)

