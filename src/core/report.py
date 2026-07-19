from datetime import datetime
from pathlib import Path



class Report:

    """
    DramaTool 整理报告生成器

    输出:
        DramaTool报告.txt

    """


    def __init__(self):

        pass



    def generate(

            self,

            project,

            output_path

    ):


        output_path = Path(
            output_path
        )


        report_file = (

            output_path

            /

            "DramaTool报告.txt"

        )



        content = []


        content.append(

            "DramaTool 整理报告"

        )


        content.append(

            "=" * 30

        )


        content.append("")



        # 项目信息

        content.append(

            f"项目:\n{project.name}"

        )


        content.append("")



        content.append(

            f"原始集数:\n{project.original_count}"

        )


        content.append(

            f"最终集数:\n{project.final_count}"

        )



        content.append("")

        content.append(

            "拆集记录:"

        )

        content.append("")



        # 拆集关系

        if project.split_map:


            for episode, parts in project.split_map.items():


                content.append(

                    f"第{episode:02d}集:"

                )


                for part in parts:


                    content.append(

                        f"    {episode:02d}-{part}"

                    )


                content.append("")


        else:


            content.append(

                "无拆集"

            )



        content.append("")

        content.append(

            "最终生成映射:"

        )

        content.append("")



        # 最终编号

        for index, source in project.episode_mapping.items():


            content.append(

                f"{index:02d} ← {source}"

            )



        content.append("")

        content.append(

            "文件统计:"

        )


        content.append("")



        for version in project.original_videos.keys():


            count = len(

                project.original_videos[version]

            )


            content.append(

                f"{version}: {count}个"

            )



        content.append("")

        content.append(

            "生成时间:"

        )


        content.append(

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )



        report_file.write_text(

            "\n".join(content),

            encoding="utf-8"

        )


        print(

            "报告生成:",

            report_file

        )


        return report_file