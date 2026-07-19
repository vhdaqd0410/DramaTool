from src.core.analyzer import Analyzer
from src.core.mapper import Mapper
from src.core.report import Report



project_path = (

    r"C:\Users\vhdaq\Desktop\DramaTest\000交付"

)



# 分析

analyzer = Analyzer(

    project_path

)


project = analyzer.analyze()


print(
    "分析完成"
)



# 映射

mapper = Mapper()

mapper.generate(

    project

)


print(

    "映射完成"

)



# 生成报告

report = Report()


report.generate(

    project,

    project_path + "_拆集版"

)