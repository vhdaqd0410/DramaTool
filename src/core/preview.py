class Preview:
    """
    DramaTool 整理预览

    显示:
    1. 项目信息
    2. 拆集关系
    3. 最终编号与来源对应关系

    示例:

    最终名称       来源

    01             01
    02             02
    03             03-1
    04             03-2
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
        # 拆集关系
        # =====================

        lines.append(
            "拆集:"
        )

        lines.append("")


        if project.split_map:


            for ep, parts in sorted(
                project.split_map.items()
            ):

                split_result = ",".join(
                    [
                        f"{ep:02d}-{p}"
                        for p in parts
                    ]
                )


                lines.append(
                    f"{ep:02d} → {split_result}"
                )


        else:

            lines.append(
                "无拆集"
            )



        lines.append("")



        # =====================
        # 最终生成
        # =====================

        lines.append(
            "最终生成:"
        )

        lines.append("")

        lines.append(
            "最终名称        来源"
        )

        lines.append(
            "----------------------------"
        )



        for final_index, source in project.episode_mapping.items():


            # 最终编号
            final_name = (
                f"{final_index:02d}"
            )


            lines.append(
                f"{final_name:<16}{source}"
            )



        return "\n".join(lines)