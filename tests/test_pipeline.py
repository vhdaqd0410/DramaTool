from src.core.pipeline import Pipeline



# ==========================
# 测试项目路径
# ==========================

project_path = (

    r"C:\Users\vhdaq\Desktop\DramaTest\000交付"

)





print("=" * 60)

print("DramaTool Pipeline 测试")

print("=" * 60)





# ==========================
# 执行完整流程
# ==========================


pipeline = Pipeline(

    project_path

)



result = pipeline.run()





print()

print("=" * 60)

print("Pipeline执行结果")

print("=" * 60)





print()


print("输出目录:")


print(

    result["output"]

)



print()


print("报告目录:")


print(

    result["report"]

)



print()


print("测试完成")