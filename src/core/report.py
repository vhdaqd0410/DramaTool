from pathlib import Path
import json
from datetime import datetime



class Report:
    """
    DramaTool 报告生成器

    输出:

    report/
        report.html
        report.json

    """



    def __init__(self, output_path):

        self.output_path = Path(output_path)

        self.report_path = (
            self.output_path
            /
            "report"
        )

        self.report_path.mkdir(
            exist_ok=True
        )



    def generate(
            self,
            project,
            check_result=None,
            mapping=None
    ):

        data = self.build_data(
            project,
            check_result,
            mapping
        )

        self.save_json(
            data
        )

        self.save_html(
            data
        )

        return self.report_path





    def build_data(
            self,
            project,
            check_result=None,
            mapping=None
    ):

        data = {

            "project": {

                "name":
                project.name,

                "original_count":
                project.original_count,

                "final_count":
                project.final_count,

                "split_count":
                len(project.split_map),

                "time":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            },


            "versions": {},


            "mapping": [],


            "check":
            check_result

        }



        # ==========================
        # 版本统计
        # ==========================

        versions = {}


        for name, files in project.original_videos.items():

            versions[name] = len(files)



        for name, files in project.split_videos.items():

            if name not in versions:

                versions[name] = 0


            versions[name] += len(files)



        data["versions"] = versions





        # ==========================
        # 集数映射
        # ==========================

        result_mapping = []



        if mapping:


            # 当前 Mapper 返回:
            #
            # {
            #    1:"01",
            #    2:"02",
            #    3:"03-1"
            # }
            #

            if isinstance(mapping, dict):


                for final, source in mapping.items():


                    result_mapping.append(

                        {

                            "final":

                            str(final).zfill(2),


                            "source":

                            source

                        }

                    )



            # 兼容未来列表结构
            #
            # [
            #   {
            #       final:"01",
            #       source:"01"
            #   }
            # ]

            else:


                for item in mapping:


                    result_mapping.append(

                        {

                            "final":

                            item["final"],


                            "source":

                            item["source"]

                        }

                    )



        data["mapping"] = result_mapping



        return data






    def save_json(
            self,
            data
    ):


        file = (

            self.report_path
            /
            "report.json"

        )


        with open(

            file,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                data,

                f,

                ensure_ascii=False,

                indent=4

            )






    def save_html(
            self,
            data
    ):


        html = []



        html.append(

"""

<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">


<title>

DramaTool整理报告

</title>


<style>

body{

font-family:

Microsoft YaHei;

padding:30px;

}


table{

border-collapse:

collapse;

width:900px;

}


td,th{

border:

1px solid #ccc;

padding:8px;

}


h1{

color:#333;

}

</style>


</head>


<body>


<h1>

DramaTool 整理报告

</h1>

"""

        )





        project = data["project"]



        html.append(

f"""

<h2>
项目概览
</h2>


<p>
项目:
{project['name']}
</p>


<p>
原始集数:
{project['original_count']}
</p>


<p>
最终集数:
{project['final_count']}
</p>


<p>
生成时间:
{project['time']}
</p>


"""

        )







        # ==========================
        # 版本统计
        # ==========================


        html.append(

"""

<h2>
版本统计
</h2>


<table>


<tr>

<th>
版本
</th>

<th>
数量
</th>

</tr>

"""

        )



        for name,count in data["versions"].items():


            html.append(

f"""

<tr>

<td>
{name}
</td>


<td>
{count}
</td>


</tr>

"""

            )



        html.append(

"""

</table>

"""

        )







        # ==========================
        # 集数映射
        # ==========================


        html.append(

"""

<h2>
集数映射
</h2>


<table>


<tr>

<th>
最终集
</th>


<th>
来源
</th>


</tr>

"""

        )





        for item in data["mapping"]:


            html.append(

f"""

<tr>

<td>
{item['final']}
</td>


<td>
{item['source']}
</td>


</tr>

"""

            )



        html.append(

"""

</table>


</body>


</html>

"""

        )





        file = (

            self.report_path
            /
            "report.html"

        )


        with open(

            file,

            "w",

            encoding="utf-8"

        ) as f:


            f.write(

                "".join(html)

            )