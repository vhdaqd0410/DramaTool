from pathlib import Path
from datetime import datetime



class Report:


    def __init__(self, output_path):


        self.output_path = Path(

            output_path

        )


        self.report_dir = (

            self.output_path

            /

            "report"

        )


        self.report_dir.mkdir(

            exist_ok=True

        )





    def generate(

            self,

            project,

            check_result

    ):


        html = self.build_html(

            project,

            check_result

        )


        file = (

            self.report_dir

            /

            "report.html"

        )


        file.write_text(

            html,

            encoding="utf-8"

        )


        return file






    def build_html(

            self,

            project,

            check_result

    ):


        # ======================
        # 集数映射
        # ======================


        mapping_rows = ""


        for final, source in sorted(

            project.episode_mapping.items()

        ):


            mapping_rows += f"""

            <tr>

            <td>
            {final:02d}
            </td>


            <td>
            {source}
            </td>


            </tr>

            """




        # ======================
        # 版本列表
        # ======================


        versions = ""


        for version in project.original_videos.keys():


            versions += f"""

            <li>
            {version}
            </li>

            """





        # ======================
        # 检查结果
        # ======================


        errors = ""


        if check_result["errors"]:


            for item in check_result["errors"]:


                errors += f"""

                <p>
                ❌ {item["version"]}
                缺少:
                {item["missing"]}
                </p>

                """

        else:


            errors = """

            <p>
            无
            </p>

            """





        warnings = ""


        if check_result["warnings"]:


            for item in check_result["warnings"]:


                warnings += f"""

                <p>
                ⚠️ {item["version"]}
                :
                {item.get("missing")}
                </p>

                """

        else:


            warnings = """

            <p>
            无
            </p>

            """








        html = f"""

<!DOCTYPE html>

<html>


<head>


<meta charset="utf-8">


<title>
DramaTool整理报告
</title>



<style>


body{{

font-family:
Microsoft YaHei;

margin:
30px;

}}



h1{{

font-size:
32px;

}}



table{{

border-collapse:
collapse;

width:
900px;

}}



td,th{{

border:
1px solid #ccc;

padding:
8px;

text-align:
center;

}}



.section{{

margin-top:
30px;

}}


</style>



</head>



<body>



<h1>
DramaTool 整理报告
</h1>



<div class="section">


<h2>
项目概览
</h2>



<p>
项目:
{project.name}
</p>



<p>
原始集数:
{project.original_count}
</p>



<p>
最终集数:
{project.final_count}
</p>



<p>
生成时间:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
</p>


</div>





<div class="section">


<h2>
检查结果
</h2>


<h3>
错误
</h3>

{errors}



<h3>
警告
</h3>

{warnings}



</div>








<div class="section">


<h2>
整理版本
</h2>



<ul>

{versions}

</ul>



</div>








<div class="section">


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


{mapping_rows}


</table>



</div>






</body>


</html>


"""


        return html