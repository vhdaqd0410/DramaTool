from src.core.analyzer import Analyzer
from src.core.mapper import Mapper
from src.core.checker import Checker
from src.core.report import Report



# ==========================
# 测试项目路径
# ==========================

project_path = (

    r"C:\Users\vhdaq\Desktop\DramaTest\000交付"

)



print("=" * 60)

print("DramaTool Report 测试")

print("=" * 60)





# ==========================
# 分析项目
# ==========================

print()

print("开始分析项目...")


analyzer = Analyzer(

    project_path

)


project = analyzer.analyze()



print("分析完成")






# ==========================
# 生成集数映射
# ==========================


print()

print("生成集数映射...")


mapper = Mapper()


mapping = mapper.generate(

    project

)


print("映射完成")







# ==========================
# 检查项目
# ==========================


print()

print("开始检查...")


checker = Checker()


check_result = checker.check(

    project

)


print("检查完成")







# ==========================
# 生成报告
# ==========================


print()

print("开始生成报告...")


report = Report(

    project_path

)



output = report.generate(

    project,

    check_result,

    mapping

)





print()

print("=" * 60)

print("报告生成完成")

print("=" * 60)


print()


print("输出目录:")


print(output)



print()


print("生成文件:")


print("✓ report.json")


print("✓ report.html")