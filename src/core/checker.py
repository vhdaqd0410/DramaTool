class Checker:
    """
    DramaTool 项目检查器 V2

    检查内容：

    1. 各视频版本完整性
    2. 字幕完整性
    3. 拆集关系正确性

    返回统一数据结构：

    {
        errors: [],
        warnings: [],
        success: []
    }

    每条记录：

    {
        level,
        version,
        type,
        files
    }

    """


    VIDEO_VERSIONS = [

        "00成片",

        "1.有音乐无字幕版本",

        "2.无音乐无字幕无bgm"

    ]


    SUBTITLE_VERSION = "3.字幕文件"



    def check(self, project):


        result = {

            "errors": [],

            "warnings": [],

            "success": []

        }


        self.check_versions(
            project,
            result
        )


        self.check_subtitles(
            project,
            result
        )


        self.check_split(
            project,
            result
        )


        return result



    # =================================
    # 检查视频版本
    # =================================

    def check_versions(
            self,
            project,
            result
    ):


        standard = set(
            range(
                1,
                project.original_count + 1
            )
        )


        for version in self.VIDEO_VERSIONS:


            if version not in project.original_videos:


                result["errors"].append({

                    "level":
                    "error",

                    "version":
                    version,

                    "type":
                    "missing_version",

                    "files":
                    []

                })

                continue



            current = set()



            for ep in project.original_videos[version]:

                current.add(
                    ep.original_episode
                )



            missing = (
                standard
                -
                current
            )



            if missing:


                files = []


                for ep in sorted(missing):

                    files.append(
                        f"{ep:02d}.mp4"
                    )



                result["errors"].append({

                    "level":
                    "error",

                    "version":
                    version,

                    "type":
                    "missing",

                    "files":
                    files

                })


            else:


                result["success"].append({

                    "level":
                    "success",

                    "version":
                    version,

                    "type":
                    "complete"

                })




    # =================================
    # 检查字幕
    # =================================

    def check_subtitles(
            self,
            project,
            result
    ):


        if self.SUBTITLE_VERSION not in project.original_videos:


            result["warnings"].append({

                "level":
                "warning",

                "version":
                self.SUBTITLE_VERSION,

                "type":
                "missing_version",

                "files":
                []

            })


            return



        standard = set(

            range(
                1,
                project.original_count + 1
            )

        )



        current = set()



        for ep in project.original_videos[
            self.SUBTITLE_VERSION
        ]:


            current.add(
                ep.original_episode
            )



        missing = (

            standard
            -
            current

        )



        if missing:


            files = []


            for ep in sorted(missing):

                files.append(
                    f"{ep:02d}.srt"
                )



            result["warnings"].append({

                "level":
                "warning",

                "version":
                self.SUBTITLE_VERSION,

                "type":
                "missing",

                "files":
                files

            })


        else:


            result["success"].append({

                "level":
                "success",

                "version":
                self.SUBTITLE_VERSION,

                "type":
                "complete"

            })




    # =================================
    # 检查拆集关系
    # =================================

    def check_split(
            self,
            project,
            result
    ):


        for ep, parts in project.split_map.items():


            parts = sorted(parts)



            expected = list(

                range(
                    1,
                    len(parts)+1
                )

            )



            if parts != expected:


                result["warnings"].append({

                    "level":
                    "warning",

                    "version":
                    "拆集关系",

                    "type":
                    "split_error",

                    "files":[

                        f"{ep:02d}拆分异常:{parts}"

                    ]

                })