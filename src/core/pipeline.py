from pathlib import Path

from src.core.analyzer import Analyzer
from src.core.mapper import Mapper
from src.core.checker import Checker
from src.core.merger import Merger
from src.core.report import Report



class Pipeline:


    def __init__(
            self,
            project_path,
            callback=None
    ):

        self.project_path = Path(
            project_path
        )

        self.output_path = None

        self.report_path = None

        # GUI消息回调
        self.callback = callback





    def log(
            self,
            message,
            progress=None
    ):

        """
        输出日志

        callback:
        message
        progress
        """

        print(message)


        if self.callback:


            self.callback(

                message,

                progress

            )







    def run(self):


        self.log(
            "开始分析项目...",
            10
        )



        analyzer = Analyzer(

            self.project_path

        )


        project = analyzer.analyze()



        self.log(

            "分析完成",

            20

        )


        self.log(

            f"项目:{project.name}",

            None

        )


        self.log(

            f"原始集数:{project.original_count}",

            None

        )


        self.log(

            f"最终集数:{project.final_count}",

            None

        )







        # =====================
        # 映射
        # =====================


        self.log(

            "生成集数映射...",

            30

        )



        mapper = Mapper()


        mapper.generate(

            project

        )


        self.log(

            "映射完成",

            40

        )








        # =====================
        # 检查
        # =====================


        self.log(

            "检查项目...",

            50

        )



        checker = Checker()



        check_result = checker.check(

            project

        )


        self.log(

            "检查完成",

            60

        )






        # 错误停止

        if check_result["errors"]:


            self.log(

                "发现错误，停止整理",

                60

            )


            for item in check_result["errors"]:


                self.log(

                    f'{item["version"]} 缺少:{item["missing"]}',

                    None

                )



            return {

                "project":

                project,


                "check":

                check_result,


                "output":

                None,


                "report":

                None

            }









        # =====================
        # 整理
        # =====================


        self.log(

            "开始整理文件...",

            70

        )


        merger = Merger(
            callback=self.callback
)



        self.output_path = merger.merge(

            project

        )



        self.log(

            "文件整理完成",

            85

        )








        # =====================
        # 报告
        # =====================


        self.log(

            "生成报告...",

            90

        )



        report = Report(

            self.output_path

        )


        report.generate(

            project,

            check_result

        )



        self.report_path = (

            Path(

                self.output_path

            )

            /

            "report"

        )



        self.log(

            "全部完成",

            100

        )



        return {


            "project":

            project,


            "check":

            check_result,


            "output":

            self.output_path,


            "report":

            self.report_path

        }