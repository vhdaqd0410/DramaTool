from src.core.analyzer import Analyzer
from src.core.checker import Checker



# ==========================
# 测试项目路径
# ==========================

project_path = (

    r"C:\Users\vhdaq\Desktop\DramaTest\000交付"

)



print("=" * 60)

print("DramaTool 检查报告 V2")

print("=" * 60)





# ==========================
# 分析项目
# ==========================


analyzer = Analyzer(

    project_path

)


project = analyzer.analyze()



print()

print(

    f"项目名称: {project.name}"

)


print(

    f"原始集数: {project.original_count}"

)


print(

    f"最终集数: {project.final_count}"

)






# ==========================
# 执行检查
# ==========================


checker = Checker()


result = checker.check(

    project

)






# ==========================
# 输出错误
# ==========================


print()

print("=" * 60)

print("检查结果")

print("=" * 60)



if result["errors"]:


    print()

    print("❌ 错误")


    for item in result["errors"]:


        print()

        print(

            f"【{item['version']}】"

        )


        if item["type"] == "missing":


            print(

                "缺少文件:"

            )


            for file in item["files"]:


                print(

                    f"   {file}"

                )


        elif item["type"] == "missing_version":


            print(

                "版本文件夹不存在"

            )



else:


    print()

    print("❌ 错误")

    print("无")








# ==========================
# 输出警告
# ==========================


if result["warnings"]:


    print()

    print("⚠ 警告")


    for item in result["warnings"]:


        print()

        print(

            f"【{item['version']}】"

        )



        if item["type"] == "missing":


            print(

                "缺少文件:"

            )


            for file in item["files"]:


                print(

                    f"   {file}"

                )


        else:


            for file in item["files"]:


                print(

                    f"   {file}"

                )



else:


    print()

    print("⚠ 警告")

    print("无")









# ==========================
# 输出完整
# ==========================


if result["success"]:


    print()

    print("✅ 完整")


    for item in result["success"]:


        print()


        print(

            f"【{item['version']}】"

        )


        print(

            "文件完整"

        )





print()

print("=" * 60)

print("检查完成")

print("=" * 60)