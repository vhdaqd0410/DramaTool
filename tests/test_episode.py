from src.models.episode import Episode


ep = Episode(
    original_episode=3,
    file_path="03-1.mp4",
    part=1
)


print(ep)

print(ep.display_name())