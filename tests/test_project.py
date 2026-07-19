from src.models.project import Project
from src.models.episode import Episode


project = Project(
    name="测试短剧",
    root_path="D:/DramaTest",
    original_count=45,
    final_count=60
)


ep1 = Episode(
    original_episode=3,
    file_path="03-1.mp4",
    part=1
)


ep2 = Episode(
    original_episode=3,
    file_path="03-2.mp4",
    part=2
)


project.add_episode(
    "00成片",
    ep1
)

project.add_episode(
    "00成片",
    ep2
)


project.add_split(
    3,
    [1,2]
)


print(project)

print(
    project.summary()
)


print(
    project.videos
)

print(
    project.split_map
)