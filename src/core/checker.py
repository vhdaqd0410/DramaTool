class Checker:


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


        self.check_subtitle(

            project,

            result

        )


        self.check_split(

            project,

            result

        )


        return result






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



            current = set()



            files = project.original_videos.get(

                version,

                []

            )



            for ep in files:


                current.add(

                    ep.original_episode

                )




            missing = sorted(

                standard - current

            )




            if missing:


                result["errors"].append(

                    {

                        "type":
                        "missing_video",


                        "version":
                        version,


                        "missing":
                        missing

                    }

                )


            else:


                result["success"].append(

                    f"{version}:完整"

                )







    def check_subtitle(

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


        current = set()



        files = project.original_videos.get(

            self.SUBTITLE_VERSION,

            []

        )



        for ep in files:


            current.add(

                ep.original_episode

            )




        missing = sorted(

            standard - current

        )




        if missing:


            result["warnings"].append(

                {

                    "type":

                    "missing_subtitle",


                    "version":

                    self.SUBTITLE_VERSION,


                    "missing":

                    missing

                }

            )


        else:


            result["success"].append(

                f"{self.SUBTITLE_VERSION}:完整"

            )







    def check_split(

        self,

        project,

        result

    ):


        for ep, parts in project.split_map.items():


            parts.sort()



            expected = list(

                range(

                    1,

                    len(parts)+1

                )

            )



            if parts != expected:


                result["warnings"].append(

                    {


                        "type":

                        "split_error",


                        "version":

                        "拆集关系",


                        "missing":

                        f"第{ep}集拆分异常"

                    }

                )