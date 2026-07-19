from src.core.analyzer import Analyzer
from src.core.mapper import Mapper
from src.core.merger import Merger


project_path = r"C:\Users\vhdaq\Desktop\DramaTest\000交付"


# =====================
# 分析项目
# =====================

analyzer = Analyzer(
    project_path
)

project = analyzer.analyze()



print("分析完成")



# =====================
# 生成映射
# =====================

mapper = Mapper()

mapper.generate(
    project
)


print("映射完成")



# =====================
# 执行整理
# =====================

merger = Merger()


output = merger.merge(
    project
)



print("================")
print("整理完成")

print(
    output
)