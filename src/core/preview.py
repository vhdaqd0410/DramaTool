class Preview:
    """
    整理预览生成器 V2

    功能:
    1. 显示项目基本信息
    2. 显示拆集关系
    3. 显示最终生成计划
    4. 显示来源文件路径
    """



    def generate(self, project):

        lines = []


        # =====================
        # 标题
        # =====================

        lines.append(
            "============================"
        )

        lines.append(
            "DramaTool 整理预览"
        )

        lines.append(
            "============================"
        )

        lines.append("")



        # =====================
        # 项目信息
        # =====================

        lines.append(
            f"项目:{project.name}"
        )


        lines.append(
            f"原始集数:{project.original_count}"
        )


        lines.append(
            f"最终集数:{project.final_count}"
        )


        lines.append("")



        # =====================
        # 拆集信息
        # =====================

        lines.append(
            "拆集:"
        )

        lines.append("")



        if project.split_map:


            for ep, parts in sorted(
                project.split_map.items()
            ):

                lines.append(
                    f"第{ep:02d}集:"
                )


                for part in parts:

                    lines.append(
                        f"  ├── {ep:02d}-{part}"
                    )


        else:

            lines.append(
                "  无拆集"
            )



        lines.append("")



        # =====================
        # 最终生成计划
        # =====================

        lines.append(
            "============================"
        )

        lines.append(
            "最终生成计划:"
        )

        lines.append(
            "============================"
        )

        lines.append("")



        # 获取来源文件

        source_map = self.build_source_map(
            project
        )



        for _, target in project.episode_mapping.items():


            source = source_map.get(
                target,
                "未知来源"
            )


            lines.append(
                f"{target}.mp4"
            )


            lines.append(
                f"  来源: {source}"
            )


            lines.append("")



        return "\n".join(lines)





    def build_source_map(
        self,
        project
    ):

        """
        建立:

        最终名称
            ↓
        来源文件

        """


        result = {}



        # =====================
        # 原始文件
        # =====================

        for version, episodes in project.original_videos.items():


            for ep in episodes:


                name = (
                    f"{ep.original_episode:02d}"
                )


                result[name] = ep.file_path





        # =====================
        # 拆集文件
        # =====================

        for version, episodes in project.split_videos.items():


            for ep in episodes:


                name = (
                    f"{ep.original_episode:02d}-{ep.part}"
                )


                result[name] = ep.file_path



        return result