class Mapper:
    """
    集数映射引擎

    根据原始交付和拆集交付
    生成最终集数编号
    """



    def generate(self, project):


        mapping = {}

        index = 1



        # 获取原始集数

        original_numbers = set()


        for episodes in project.original_videos.values():

            for ep in episodes:

                original_numbers.add(
                    ep.original_episode
                )



        # 按原始集数排序

        for old_ep in sorted(original_numbers):


            # 判断是否拆集

            if old_ep in project.split_map:


                parts = sorted(
                    project.split_map[old_ep]
                )


                for part in parts:


                    mapping[index] = (
                        f"{old_ep:02d}-{part}"
                    )

                    index += 1



            else:


                mapping[index] = (
                    f"{old_ep:02d}"
                )

                index += 1



        project.episode_mapping = mapping


        project.final_count = len(
            mapping
        )


        return mapping