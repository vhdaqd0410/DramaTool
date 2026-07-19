from src.core.analyzer import Analyzer
from src.core.mapper import Mapper


path = r"C:\Users\vhdaq\Desktop\DramaTest\000交付"


print("开始分析项目...")


project = Analyzer(path).analyze()


print("分析完成")

print()

print("原始集数:")
print(project.original_count)

print()

print("拆集关系:")
print(project.split_map)


print()
print("================")


mapper = Mapper()


result = mapper.generate(
    project
)


print(
    "最终集数:",
    project.final_count
)


print()


print("最终映射:")


for key, value in result.items():

    print(
        key,
        "→",
        value
    )