from pathlib import Path

from src.core.analyzer import Analyzer
from src.core.mapper import Mapper
from src.core.checker import Checker
from src.core.merger import Merger
from src.core.report import Report



class Pipeline:


    """
    DramaTool 自动整理流程

    流程:

    Analyzer
        ↓
    Mapper
        ↓
    Checker
        ↓
    Merger
        ↓
    Report

    """



    def __init__(self, project_path):


        self.project_path = Path(
            project_path
        )


        self.project = None

        self.mapping = None

        self.check_result = None

        self.output_path = None

        self.report_path = None





    def run(self):


        print("=" * 50)

        print(
            "DramaTool 自动整理"
        )

        print("=" * 50)



        # ======================
        # 分析项目
        # ======================


        print()

        print(
            "开始分析项目..."
        )


        analyzer = Analyzer(

            self.project_path

        )


        self.project = analyzer.analyze()


        print(
            "分析完成"
        )


        print(
            f"项目: {self.project.name}"
        )


        print(
            f"原始集数: {self.project.original_count}"
        )


        print(
            f"最终集数: {self.project.final_count}"
        )





        # ======================
        # 生成映射
        # ======================


        print()

        print(
            "生成集数映射..."
        )


        mapper = Mapper()


        self.mapping = mapper.generate(

            self.project

        )


        print(
            "映射完成"
        )





        # ======================
        # 检查项目
        # ======================


        print()

        print(
            "检查项目..."
        )


        checker = Checker()


        self.check_result = checker.check(

            self.project

        )


        print(
            "检查完成"
        )



        # ======================
        # 有错误停止
        # ======================


        if self.check_result["errors"]:


            print()

            print(
                "================"
            )

            print(
                "发现错误，停止整理"
            )

            print(
                "================"
            )


            for error in self.check_result["errors"]:


                print()

                print(
                    "版本:",
                    error.get(
                        "version"
                    )
                )


                print(
                    "缺少:",
                    error.get(
                        "missing"
                    )
                )


            return {


                "project":
                self.project,


                "mapping":
                self.mapping,


                "check":
                self.check_result,


                "output":
                None,


                "report":
                None

            }






        # ======================
        # 文件整理
        # ======================


        print()

        print(
            "开始整理文件..."
        )


        merger = Merger()


        self.output_path = merger.merge(

            self.project

        )


        print()

        print(
            "整理完成:"
        )


        print(
            self.output_path
        )





        # ======================
        # 生成报告
        # ======================


        print()

        print(
            "生成报告..."
        )


        report = Report()


        self.report_path = report.generate(

            self.project,

            self.mapping,

            self.check_result,

            self.output_path

        )


        print()

        print(
            "报告生成完成:"
        )


        print(
            self.report_path
        )




        return {


            "project":
            self.project,


            "mapping":
            self.mapping,


            "check":
            self.check_result,


            "output":
            self.output_path,


            "report":
            self.report_path

        }