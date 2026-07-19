import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

import threading
import os

from src.core.pipeline import Pipeline



class DramaToolApp:


    def __init__(self, root):

        self.root = root

        self.root.title(
            "DramaTool 拆集整理工具"
        )

        self.root.geometry(
            "900x650"
        )


        self.project_path = None

        self.output_path = None


        self.create_ui()



    def create_ui(self):


        top = tk.Frame(
            self.root
        )

        top.pack(
            pady=20
        )



        self.path_label = tk.Label(

            top,

            text="请选择项目",

            width=70

        )


        self.path_label.pack(

            side=tk.LEFT,

            padx=10

        )



        tk.Button(

            top,

            text="选择项目",

            command=self.select_project

        ).pack(

            side=tk.LEFT

        )






        self.start_btn = tk.Button(

            self.root,

            text="开始整理",

            width=20,

            height=2,

            command=self.start

        )


        self.start_btn.pack(

            pady=10

        )






        self.progress = ttk.Progressbar(

            self.root,

            length=700,

            mode="determinate"

        )


        self.progress.pack(

            pady=10

        )



        self.status = tk.Label(

            self.root,

            text="等待操作"

        )


        self.status.pack()






        self.log_box = tk.Text(

            self.root,

            height=25

        )


        self.log_box.pack(

            fill=tk.BOTH,

            expand=True,

            padx=20,

            pady=10

        )







    def select_project(self):


        path = filedialog.askdirectory()


        if path:


            self.project_path = path


            self.path_label.config(

                text=path

            )







    def write_log(

            self,

            message,

            progress=None

    ):


        def update():


            if progress is not None:


                self.progress["value"] = progress


                self.status.config(

                    text=f"当前进度:{progress}%"

                )



            self.log_box.insert(

                tk.END,

                message + "\n"

            )


            self.log_box.see(

                tk.END

            )



        self.root.after(

            0,

            update

        )








    def start(self):


        if not self.project_path:


            messagebox.showwarning(

                "提示",

                "请先选择项目"

            )

            return




        self.start_btn.config(

            state=tk.DISABLED

        )


        self.progress["value"]=0


        self.log_box.delete(

            "1.0",

            tk.END

        )



        threading.Thread(

            target=self.run_pipeline

        ).start()







    def run_pipeline(self):


        try:


            pipeline = Pipeline(

                self.project_path,

                callback=self.write_log

            )


            result = pipeline.run()



            if result["output"]:


                self.output_path = result["output"]



                self.write_log(

                    "整理成功",

                    100

                )



                self.root.after(

                    0,

                    self.show_complete_window

                )



            else:


                self.root.after(

                    0,

                    lambda:

                    messagebox.showwarning(

                        "整理失败",

                        "项目检查未通过，请查看日志"

                    )

                )



        except Exception as e:


            self.root.after(

                0,

                lambda:

                messagebox.showerror(

                    "运行错误",

                    str(e)

                )

            )



        finally:


            self.root.after(

                0,

                lambda:

                self.start_btn.config(

                    state=tk.NORMAL

                )

            )









    def show_complete_window(self):


        win = tk.Toplevel(

            self.root

        )


        win.title(

            "整理完成"

        )


        win.geometry(

            "500x220"

        )


        win.resizable(

            False,

            False

        )



        tk.Label(

            win,

            text="✅ 整理完成！",

            font=(

                "Microsoft YaHei",

                18

            )

        ).pack(

            pady=20

        )



        tk.Label(

            win,

            text=self.output_path,

            wraplength=450

        ).pack(

            pady=10

        )




        btn_frame = tk.Frame(

            win

        )


        btn_frame.pack(

            pady=20

        )




        tk.Button(

            btn_frame,

            text="打开目录",

            width=15,

            command=lambda:

            os.startfile(

                self.output_path

            )

        ).pack(

            side=tk.LEFT,

            padx=20

        )





        tk.Button(

            btn_frame,

            text="关闭",

            width=15,

            command=win.destroy

        ).pack(

            side=tk.LEFT,

            padx=20

        )






if __name__ == "__main__":


    root = tk.Tk()


    app = DramaToolApp(

        root

    )


    root.mainloop()