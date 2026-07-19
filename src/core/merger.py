import os
import shutil



class Merger:


    """
    DramaTool 文件整理模块


    增加:
        callback(message, progress)

    用于GUI实时显示进度

    """



    VERSIONS = [

        "00成片",

        "1.有音乐无字幕版本",

        "2.无音乐无字幕无bgm",

        "3.字幕文件"

    ]





    def __init__(self, callback=None):


        self.callback = callback





    def log(

            self,

            message,

            progress=None

    ):


        print(message)


        if self.callback:


            self.callback(

                message,

                progress

            )







    def merge(

            self,

            project

    ):


        root_path = project.root_path


        if not root_path:


            raise Exception(

                "项目路径为空"

            )



        output_path = (

            root_path.rstrip("\\/")

            +

            "_拆集版"

        )



        self.log(

            f"输出目录:{output_path}",

            70

        )



        self.create_dirs(

            output_path

        )




        total = len(self.VERSIONS)

        current = 0



        for version in self.VERSIONS:


            current += 1



            progress = (

                70

                +

                int(

                    current / total * 15

                )

            )



            self.log(

                f"正在处理:{version}",

                progress

            )



            self.merge_version(

                project,

                version,

                output_path

            )



        self.log(

            "文件整理完成",

            85

        )


        return output_path







    def create_dirs(

            self,

            output_path

    ):


        for version in self.VERSIONS:


            folder = os.path.join(

                output_path,

                version

            )


            os.makedirs(

                folder,

                exist_ok=True

            )










    def merge_version(

            self,

            project,

            version,

            output_path

    ):



        files = self.collect_files(

            project,

            version

        )



        target_dir = os.path.join(

            output_path,

            version

        )



        total = len(

            project.episode_mapping

        )


        index = 0



        for final_index, source_name in project.episode_mapping.items():


            index += 1



            progress = 70 + int(

                index / total * 15

            )



            source_file = files.get(

                source_name

            )



            if not source_file:


                self.log(

                    f"缺少文件:{source_name}",

                    progress

                )

                continue





            ext = os.path.splitext(

                source_file

            )[1]



            target_name = (

                f"{final_index:02d}{ext}"

            )



            target_file = os.path.join(

                target_dir,

                target_name

            )



            shutil.copy2(

                source_file,

                target_file

            )



            self.log(

                f"复制:{source_name} → {target_name}",

                progress

            )










    def collect_files(

            self,

            project,

            version

    ):


        result = {}




        if version in project.original_videos:


            for item in project.original_videos[version]:


                result[

                    item.display_name()

                ] = item.file_path






        if version in project.split_videos:


            for item in project.split_videos[version]:


                result[

                    item.display_name()

                ] = item.file_path





        return result