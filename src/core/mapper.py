class Mapper:
    """
    集数映射器
    """


    def generate(self, project):

        mapping = {}

        new_index = 1


        # 默认按照原集顺序

        original = {}


        for version, episodes in project.videos.items():

            for ep in episodes:

                key = ep.original_episode


                if key not in original:

                    original[key] = []


                original[key].append(ep)



        # 排序原始集数

        for old_ep in sorted(original.keys()):


            items = original[old_ep]


            # 有拆集

            parts = [
                x for x in items
                if x.part > 0
            ]


            if parts:

                parts.sort(
                    key=lambda x:x.part
                )


                for p in parts:

                    mapping[new_index] = (
                        f"{old_ep:02d}-{p.part}"
                    )

                    new_index += 1


            else:


                mapping[new_index] = (
                    f"{old_ep:02d}"
                )

                new_index += 1



        project.episode_mapping = mapping

        project.final_count = (
            len(mapping)
        )


        return mapping