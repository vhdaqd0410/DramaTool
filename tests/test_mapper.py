from src.core.analyzer import Analyzer
from src.core.mapper import Mapper


path = r"C:\Users\vhdaq\Desktop\DramaTest\000交付"


project = Analyzer(path).analyze()


mapper = Mapper()


result = mapper.generate(
    project
)


print("================")

print(
    "最终集数:",
    project.final_count
)


print()

for k,v in result.items():

    print(
        k,
        "→",
        v
    )