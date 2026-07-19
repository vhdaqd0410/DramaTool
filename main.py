import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from pathlib import Path
import os

from src.core.pipeline import Pipeline



class DramaToolApp:


    def __init__(self, root):

        self.root = root

        self.root.title(
            "DramaTool 拆集整理工具"
        )

        self.root.geometry(
            "700x500"
        )


        self.project_path = None


        self.create_ui()





    def create_ui(self):


        frame = tk.Frame(
            self.root
        )

        frame.pack(
            pady=10
        )



        self.path_label = tk.Label(

            frame,

            text="未选择项目"

        )


        self.path_label.pack(

            side=tk.LEFT,

            padx=10

        )



        btn = tk.Button(

            frame,

            text="选择项目",

            command=self.select_folder

        )


        btn.pack(

            side=tk.LEFT

        )





        start_btn = tk.Button(

            self.root,

            text="开始整理",

            width=20,

            height=2,

            command=self.start

        )


        start_btn.pack(

            pady=10

        )





        self.log = scrolledtext.ScrolledText(

            self.root,

            width=80,

            height=20

        )


        self.log.pack(

            padx=10,

            pady=10

        )







    def write_log(
        self,
        text
    ):


        self.log.insert(

            tk.END,

            text + "\n"

        )


        self.log.see(

            tk.END

        )


        self.root.update()






    def select_folder(self):


        path = filedialog.askdirectory()



        if path:


            self.project_path = Path(

                path

            )


            self.path_label.config(

                text=str(path)

            )


            self.write_log(

                "选择项目: "

                + str(path)

            )







    def start(self):


        if not self.project_path:


            messagebox.showwarning(

                "提示",

                "请先选择项目目录"

            )

            return




        self.log.delete(

            "1.0",

            tk.END

        )



        self.write_log(

            "开始执行..."

        )




        try:



            pipeline = Pipeline(

                self.project_path

            )



            result = pipeline.run()





            # ======================
            # 检查失败
            # ======================


            if not result["output"]:


                self.show_error_window(

                    result["project"],

                    result["check"]["errors"]

                )


                return





            messagebox.showinfo(

                "完成",

                "整理完成\n\n"

                + str(

                    result["output"]

                )

            )





        except Exception as e:


            messagebox.showerror(

                "错误",

                str(e)

            )









    def show_error_window(

            self,

            project,

            errors

    ):


        win = tk.Toplevel(

            self.root

        )


        win.title(

            "项目检查失败"

        )


        win.geometry(

            "550x450"

        )



        title = tk.Label(

            win,

            text="发现缺失文件，请补齐后重新执行",

            font=(

                "微软雅黑",

                12,

                "bold"

            )

        )


        title.pack(

            pady=10

        )






        for error in errors:



            frame = tk.Frame(

                win,

                relief="groove",

                borderwidth=1

            )


            frame.pack(

                fill="x",

                padx=20,

                pady=8

            )




            missing_text = ""



            for ep in error["missing"]:


                missing_text += (

                    f"第{int(ep):02d}集\n"

                )




            label = tk.Label(

                frame,

                text=(

                    "❌ "

                    + error["version"]

                    + "\n\n缺少:\n"

                    + missing_text

                ),

                justify="left",

                anchor="w"

            )


            label.pack(

                side="left",

                padx=10,

                pady=10

            )






            def open_folder(

                    version=error["version"]

            ):


                folder = Path(

                    project.root_path

                ) / version




                if folder.exists():


                    os.startfile(

                        folder

                    )


                else:


                    messagebox.showwarning(

                        "提示",

                        "目录不存在"

                    )






            btn = tk.Button(

                frame,

                text="打开目录",

                command=open_folder

            )


            btn.pack(

                side="right",

                padx=10

            )







        close = tk.Button(

            win,

            text="关闭",

            command=win.destroy

        )


        close.pack(

            pady=15

        )







if __name__ == "__main__":


    root = tk.Tk()


    app = DramaToolApp(

        root

    )


    root.mainloop()