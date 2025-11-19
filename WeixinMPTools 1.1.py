__version__ = "1.1"

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
from pathlib import Path
import math
import requests
import re
import sys
import tempfile
import time
import threading
from datetime import datetime
from packaging import version
import pyperclip
import io
import webbrowser
import base64


def check_for_updates(current_version: str, repo: str = "SorakageMeiou/WeixinMPTools", root=None):
    try:
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        release_info = response.json()

        latest_tag = release_info["tag_name"].lstrip("v")  # 去掉 'v' 前缀
        latest_name = release_info.get("name", latest_tag)
        download_url = release_info["html_url"] 

        if version.parse(latest_tag) > version.parse(current_version):
            def show_update_dialog():
                msg = f"发现新版本：{latest_name}\n\n当前版本：{current_version}\n最新版本：{latest_tag}\n\n是否前往下载页面更新？"
                if messagebox.askyesno("发现更新", msg):
                    webbrowser.open(download_url)

            if root:
                root.after(0, show_update_dialog) 
            else:
                show_update_dialog() 
        else:
            # 没有更新时也显示提示
            def show_no_update_dialog():
                messagebox.showinfo("检查更新", f"当前已是最新版本：{current_version}")

            if root:
                root.after(0, show_no_update_dialog)

    except Exception as e:
        # 检查更新失败时显示错误信息
        def show_error_dialog():
            messagebox.showerror("检查更新失败", f"无法检查更新：{str(e)}")
        
        if root:
            root.after(0, show_error_dialog)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class WeChatTools:
    def __init__(self, root):
        self.root = root
        self.root.title("公众号工具集 @SoraKaGe_MeiOu")
        self.root.state('zoomed')
        self.root.geometry("1200x700")
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                print(f"图标文件未找到: {icon_path}")
        except Exception as e:
            print(f"加载图标失败: {e}")
        self.root.minsize(1000, 600)  

        # 显示更新检查提示
        self.show_update_check_dialog()

        # 创建选项卡
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.stitch_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stitch_frame, text="图片拼接")
        
        self.extract_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.extract_frame, text="封面图提取")
        
        self.compress_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.compress_frame, text="图片压缩")
        
        # 初始化
        self.init_image_stitching_tool()
        self.init_cover_extraction_tool()
        self.init_image_compressor_tool()
        
        # 底部状态栏和GitHub按钮
        self.create_bottom_bar()
        
    def show_update_check_dialog(self):
        """显示更新检查对话框"""
        self.update_dialog = tk.Toplevel(self.root)
        self.update_dialog.title("检查更新")
        self.update_dialog.geometry("300x120")
        self.update_dialog.resizable(False, False)
        self.update_dialog.transient(self.root)  # 设置为父窗口的临时窗口
        self.update_dialog.grab_set()  # 模态对话框
        
        # 居中显示
        self.update_dialog.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.update_dialog.winfo_width()) // 2
        y = (self.root.winfo_screenheight() - self.update_dialog.winfo_height()) // 2
        self.update_dialog.geometry(f"+{x}+{y}")
        
        # 添加内容
        ttk.Label(self.update_dialog, text="正在检查更新...", font=("Arial", 10)).pack(pady=20)
        self.update_status = ttk.Label(self.update_dialog, text="连接服务器中...", font=("Arial", 9))
        self.update_status.pack(pady=10)
        
        # 启动更新检查
        threading.Thread(target=self.background_update_check, daemon=True).start()
    
    def background_update_check(self):
        """后台检查更新"""
        try:
            self.update_status.config(text="正在检查 GitHub 版本...")
            check_for_updates(__version__, repo="SorakageMeiou/WeixinMPTools", root=self.root)
        except Exception as e:
            # 更新检查失败
            def show_final_error():
                self.update_status.config(text=f"检查失败: {str(e)}")
                # 2秒后自动关闭
                self.root.after(2000, self.update_dialog.destroy)
            
            self.root.after(0, show_final_error)
        else:
            # 更新检查完成（无论是否有更新）
            def close_dialog():
                self.update_dialog.destroy()
            
            self.root.after(0, close_dialog)

    def create_bottom_bar(self):
        # 底部状态栏和GitHub按钮区域
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        bottom_frame.grid_columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="就绪")
        self.status_bar = ttk.Label(bottom_frame, textvariable=self.status_var, 
                                  relief="sunken", padding=(5, 2), foreground="black")
        self.status_bar.grid(row=0, column=0, sticky="ew")
        
        # GitHub按钮
        github_button = ttk.Button(bottom_frame, text="GitHub", command=self.open_github)
        github_button.grid(row=0, column=1, padx=(5, 0), pady=2)
    
    def open_github(self):
        webbrowser.open("https://github.com/SorakageMeiou")
    
    def set_error_status(self, message):
        self.status_var.set(message)
        self.status_bar.config(foreground="red")
        self.root.after(5000, lambda: self.status_bar.config(foreground="black"))

    # ==================== 图片拼接工具 ====================
    def init_image_stitching_tool(self):
        # 初始化
        self.top_image_path = None
        self.bottom_image_path = None
        self.top_image = None
        self.bottom_image = None
        self.top_cropped = None
        self.bottom_cropped = None
        self.stitched_image = None
        
        # 裁剪
        self.top_crop_start = None
        self.top_crop_end = None
        self.bottom_crop_start = None
        self.bottom_crop_end = None
        self.drawing_top = False
        self.drawing_bottom = False
        
        # 裁剪比例
        self.top_ratio = 2.35  # 上方图比例
        self.bottom_ratio = 1.0  # 下方图比例
        
        # 背景选项
        self.bg_var = tk.StringVar(value="white")
        
        self.create_stitching_widgets()
        
    def create_stitching_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.stitch_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧控制面板
        control_frame = ttk.Frame(main_frame, width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)
        
        # 图片选择区域
        select_frame = ttk.LabelFrame(control_frame, text="图片选择", padding=10)
        select_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 上方图选择
        ttk.Label(select_frame, text="上方图 (2.35:1):").pack(anchor=tk.W)
        top_select_frame = ttk.Frame(select_frame)
        top_select_frame.pack(fill=tk.X, pady=(5, 10))
        ttk.Button(top_select_frame, text="选择图片", 
                  command=self.select_top_image).pack(side=tk.LEFT)
        self.top_status = ttk.Label(top_select_frame, text="未选择", foreground="red")
        self.top_status.pack(side=tk.LEFT, padx=(10, 0))
        
        # 下方图选择
        ttk.Label(select_frame, text="下方图 (1:1):").pack(anchor=tk.W)
        bottom_select_frame = ttk.Frame(select_frame)
        bottom_select_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(bottom_select_frame, text="选择图片", 
                  command=self.select_bottom_image).pack(side=tk.LEFT)
        self.bottom_status = ttk.Label(bottom_select_frame, text="未选择", foreground="red")
        self.bottom_status.pack(side=tk.LEFT, padx=(10, 0))
        
        # 裁剪设置区域
        crop_frame = ttk.LabelFrame(control_frame, text="裁剪设置", padding=10)
        crop_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(crop_frame, text="上方图裁剪 (2.35:1):").pack(anchor=tk.W)
        crop_top_frame = ttk.Frame(crop_frame)
        crop_top_frame.pack(fill=tk.X, pady=(5, 10))
        ttk.Button(crop_top_frame, text="开始裁剪", 
                  command=self.start_top_crop).pack(side=tk.LEFT)
        ttk.Button(crop_top_frame, text="应用裁剪", 
                  command=self.apply_top_crop).pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Label(crop_frame, text="下方图裁剪 (1:1):").pack(anchor=tk.W)
        crop_bottom_frame = ttk.Frame(crop_frame)
        crop_bottom_frame.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(crop_bottom_frame, text="开始裁剪", 
                  command=self.start_bottom_crop).pack(side=tk.LEFT)
        ttk.Button(crop_bottom_frame, text="应用裁剪", 
                  command=self.apply_bottom_crop).pack(side=tk.LEFT, padx=(5, 0))
        
        # 拼接设置区域
        stitch_frame = ttk.LabelFrame(control_frame, text="拼接设置", padding=10)
        stitch_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 背景选择
        bg_frame = ttk.Frame(stitch_frame)
        bg_frame.pack(fill=tk.X, pady=5)
        ttk.Label(bg_frame, text="背景:").pack(side=tk.LEFT)
        ttk.Radiobutton(bg_frame, text="白色", variable=self.bg_var, 
                       value="white", command=self.update_stitch_preview).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Radiobutton(bg_frame, text="透明", variable=self.bg_var, 
                       value="transparent", command=self.update_stitch_preview).pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(stitch_frame, text="执行拼接", 
                  command=self.stitch_images).pack(pady=5)
        
        # 保存区域
        save_frame = ttk.LabelFrame(control_frame, text="保存结果", padding=10)
        save_frame.pack(fill=tk.X)
        
        ttk.Button(save_frame, text="保存图片", 
                  command=self.save_image).pack(pady=5)
        
        # 右侧预览区域
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 原始图预览
        orig_preview_frame = ttk.LabelFrame(preview_frame, text="原始图预览", padding=10)
        orig_preview_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 创建左右分栏的框架
        self.orig_split_frame = ttk.Frame(orig_preview_frame)
        self.orig_split_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧上方图画布
        self.top_canvas_frame = ttk.LabelFrame(self.orig_split_frame, text="上方图 (2.35:1)")
        self.top_canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.top_canvas = tk.Canvas(self.top_canvas_frame, bg="white")
        self.top_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 右侧下方图画布
        self.bottom_canvas_frame = ttk.LabelFrame(self.orig_split_frame, text="下方图 (1:1)")
        self.bottom_canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.bottom_canvas = tk.Canvas(self.bottom_canvas_frame, bg="white")
        self.bottom_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 处理后预览
        processed_preview_frame = ttk.LabelFrame(preview_frame, text="处理后预览", padding=10)
        processed_preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建画布用于显示处理后的图片
        self.processed_canvas = tk.Canvas(processed_preview_frame, bg="white")
        self.processed_canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.top_canvas.bind("<ButtonPress-1>", self.on_top_canvas_press)
        self.top_canvas.bind("<B1-Motion>", self.on_top_canvas_drag)
        self.top_canvas.bind("<ButtonRelease-1>", self.on_top_canvas_release)
        
        self.bottom_canvas.bind("<ButtonPress-1>", self.on_bottom_canvas_press)
        self.bottom_canvas.bind("<B1-Motion>", self.on_bottom_canvas_drag)
        self.bottom_canvas.bind("<ButtonRelease-1>", self.on_bottom_canvas_release)
        
        # 绑定窗口大小变化事件
        self.root.bind("<Configure>", self.on_window_resize)
        
    def select_top_image(self):
        file_path = filedialog.askopenfilename(
            title="选择上方图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.top_image_path = file_path
            self.top_image = Image.open(file_path)
            self.top_status.config(text=os.path.basename(file_path), foreground="green")
            self.update_original_preview()
            
    def select_bottom_image(self):
        file_path = filedialog.askopenfilename(
            title="选择下方图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.bottom_image_path = file_path
            self.bottom_image = Image.open(file_path)
            self.bottom_status.config(text=os.path.basename(file_path), foreground="green")
            self.update_original_preview()
            
    def update_original_preview(self):
        # 清空所有画布
        self.top_canvas.delete("all")
        self.bottom_canvas.delete("all")
        
        # 更新上方图预览
        if self.top_image:
            # 计算画布尺寸
            canvas_width = self.top_canvas.winfo_width()
            canvas_height = self.top_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                # 如果画布还没有实际尺寸，等待一下再更新
                self.root.after(100, self.update_original_preview)
                return
            
            # 缩放图片以适应画布
            top_img = self.top_image.copy()
            top_img.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
            self.top_photo = ImageTk.PhotoImage(top_img)
            
            # 计算居中位置
            x = (canvas_width - top_img.width) // 2
            y = (canvas_height - top_img.height) // 2
            
            self.top_canvas.create_image(x, y, anchor=tk.NW, image=self.top_photo, tags="top_image")
        
        # 更新下方图预览
        if self.bottom_image:
            # 计算画布尺寸
            canvas_width = self.bottom_canvas.winfo_width()
            canvas_height = self.bottom_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                # 如果画布还没有实际尺寸，等待一下再更新
                self.root.after(100, self.update_original_preview)
                return
            
            # 缩放图片以适应画布
            bottom_img = self.bottom_image.copy()
            bottom_img.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
            self.bottom_photo = ImageTk.PhotoImage(bottom_img)
            
            # 计算居中位置
            x = (canvas_width - bottom_img.width) // 2
            y = (canvas_height - bottom_img.height) // 2
            
            self.bottom_canvas.create_image(x, y, anchor=tk.NW, image=self.bottom_photo, tags="bottom_image")
    
    def update_stitch_preview(self):
        self.processed_canvas.delete("all")
        
        if self.stitched_image:
            # 计算画布尺寸
            canvas_width = self.processed_canvas.winfo_width()
            canvas_height = self.processed_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                # 如果画布还没有实际尺寸，等待一下再更新
                self.root.after(100, self.update_stitch_preview)
                return
            
            # 缩放图片以适应画布
            img = self.stitched_image.copy()
            img.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
            self.stitched_photo = ImageTk.PhotoImage(img)
            
            # 计算居中位置
            x = (canvas_width - img.width) // 2
            y = (canvas_height - img.height) // 2
            
            self.processed_canvas.create_image(x, y, anchor=tk.NW, image=self.stitched_photo)
    
    def start_top_crop(self):
        if not self.top_image:
            messagebox.showwarning("警告", "请先选择上方图片")
            return
        
        self.drawing_top = True
        self.top_crop_start = None
        self.top_crop_end = None
        messagebox.showinfo("提示", "请在上方图画布上拖动鼠标绘制裁剪区域")
    
    def start_bottom_crop(self):
        if not self.bottom_image:
            messagebox.showwarning("警告", "请先选择下方图片")
            return
        
        self.drawing_bottom = True
        self.bottom_crop_start = None
        self.bottom_crop_end = None
        messagebox.showinfo("提示", "请在下方图画布上拖动鼠标绘制裁剪区域")
    
    def on_top_canvas_press(self, event):
        if self.drawing_top:
            self.top_crop_start = (event.x, event.y)
            self.top_crop_end = (event.x, event.y)
    
    def on_top_canvas_drag(self, event):
        if self.drawing_top and self.top_crop_start:
            self.top_canvas.delete("top_crop_rect")
            x1, y1 = self.top_crop_start
            x2, y2 = event.x, event.y
            
            # 计算固定比例的裁剪框
            width = x2 - x1
            height = y2 - y1
            
            # 根据比例调整尺寸
            if abs(width) > abs(height) * self.top_ratio:
                # 宽度过大，调整高度
                height = abs(width) / self.top_ratio
                if y2 < y1:
                    height = -height
            else:
                # 高度过大，调整宽度
                width = abs(height) * self.top_ratio
                if x2 < x1:
                    width = -width
            
            x2 = x1 + width
            y2 = y1 + height
            
            self.top_crop_end = (x2, y2)
            self.top_canvas.create_rectangle(x1, y1, x2, y2, outline="red", dash=(4, 4), tags="top_crop_rect")
    
    def on_top_canvas_release(self, event):
        # 释放事件已经在拖动中处理了
        pass
    
    def on_bottom_canvas_press(self, event):
        if self.drawing_bottom:
            self.bottom_crop_start = (event.x, event.y)
            self.bottom_crop_end = (event.x, event.y)
    
    def on_bottom_canvas_drag(self, event):
        if self.drawing_bottom and self.bottom_crop_start:
            self.bottom_canvas.delete("bottom_crop_rect")
            x1, y1 = self.bottom_crop_start
            x2, y2 = event.x, event.y
            
            # 计算固定比例的裁剪框
            width = x2 - x1
            height = y2 - y1
            
            # 根据1:1比例调整尺寸
            size = max(abs(width), abs(height))
            
            if abs(width) > abs(height):
                # 宽度更大，调整高度
                height = size
                if y2 < y1:
                    height = -height
            else:
                # 高度更大，调整宽度
                width = size
                if x2 < x1:
                    width = -width
            
            x2 = x1 + width
            y2 = y1 + height
            
            self.bottom_crop_end = (x2, y2)
            self.bottom_canvas.create_rectangle(x1, y1, x2, y2, outline="red", dash=(4, 4), tags="bottom_crop_rect")
    
    def on_bottom_canvas_release(self, event):
        # 释放事件已经在拖动中处理了
        pass
    
    def apply_top_crop(self):
        if not self.top_crop_start or not self.top_crop_end:
            messagebox.showwarning("警告", "请先绘制裁剪区域")
            return
        
        # 获取画布上图片的实际位置和尺寸
        canvas_items = self.top_canvas.find_withtag("top_image")
        if not canvas_items:
            messagebox.showwarning("警告", "无法找到上方图片")
            return
        
        # 获取图片在画布上的位置
        bbox = self.top_canvas.bbox(canvas_items[0])
        img_x, img_y, img_x2, img_y2 = bbox
        img_width = img_x2 - img_x
        img_height = img_y2 - img_y
        
        # 计算裁剪区域相对于原始图片的比例
        x1, y1 = self.top_crop_start
        x2, y2 = self.top_crop_end
        
        # 确保x1<x2, y1<y2
        crop_x1 = min(x1, x2)
        crop_y1 = min(y1, y2)
        crop_x2 = max(x1, x2)
        crop_y2 = max(y1, y2)
        
        # 计算相对于图片的裁剪区域
        rel_x1 = max(0, crop_x1 - img_x)
        rel_y1 = max(0, crop_y1 - img_y)
        rel_x2 = min(img_width, crop_x2 - img_x)
        rel_y2 = min(img_height, crop_y2 - img_y)
        
        # 检查裁剪区域是否有效
        if rel_x2 - rel_x1 < 50 or rel_y2 - rel_y1 < 50:
            messagebox.showwarning("警告", "裁剪区域过小，请选择更大的区域")
            return
        
        # 计算原始图片与显示图片的比例
        scale_x = self.top_image.width / img_width
        scale_y = self.top_image.height / img_height
        
        # 计算原始图片上的裁剪区域
        orig_x1 = int(rel_x1 * scale_x)
        orig_y1 = int(rel_y1 * scale_y)
        orig_x2 = int(rel_x2 * scale_x)
        orig_y2 = int(rel_y2 * scale_y)
        
        # 应用裁剪
        self.top_cropped = self.top_image.crop((orig_x1, orig_y1, orig_x2, orig_y2))
        
        # 确保比例为2.35:1
        target_height = int(self.top_cropped.width / self.top_ratio)
        if target_height > self.top_cropped.height:
            # 如果高度不足，调整宽度
            target_width = int(self.top_cropped.height * self.top_ratio)
            left = (self.top_cropped.width - target_width) // 2
            self.top_cropped = self.top_cropped.crop((left, 0, left + target_width, self.top_cropped.height))
        else:
            # 如果高度足够，调整高度
            top = (self.top_cropped.height - target_height) // 2
            self.top_cropped = self.top_cropped.crop((0, top, self.top_cropped.width, top + target_height))
        
        self.drawing_top = False
        self.top_canvas.delete("top_crop_rect")
        messagebox.showinfo("成功", "上方图裁剪完成")
    
    def apply_bottom_crop(self):
        if not self.bottom_crop_start or not self.bottom_crop_end:
            messagebox.showwarning("警告", "请先绘制裁剪区域")
            return
        
        # 获取画布上图片的实际位置和尺寸
        canvas_items = self.bottom_canvas.find_withtag("bottom_image")
        if not canvas_items:
            messagebox.showwarning("警告", "无法找到下方图片")
            return
        
        # 获取图片在画布上的位置
        bbox = self.bottom_canvas.bbox(canvas_items[0])
        img_x, img_y, img_x2, img_y2 = bbox
        img_width = img_x2 - img_x
        img_height = img_y2 - img_y
        
        # 计算裁剪区域相对于原始图片的比例
        x1, y1 = self.bottom_crop_start
        x2, y2 = self.bottom_crop_end
        
        # 确保x1<x2, y1<y2
        crop_x1 = min(x1, x2)
        crop_y1 = min(y1, y2)
        crop_x2 = max(x1, x2)
        crop_y2 = max(y1, y2)
        
        # 计算相对于图片的裁剪区域
        rel_x1 = max(0, crop_x1 - img_x)
        rel_y1 = max(0, crop_y1 - img_y)
        rel_x2 = min(img_width, crop_x2 - img_x)
        rel_y2 = min(img_height, crop_y2 - img_y)
        
        # 检查裁剪区域是否有效
        if rel_x2 - rel_x1 < 50 or rel_y2 - rel_y1 < 50:
            messagebox.showwarning("警告", "裁剪区域过小，请选择更大的区域")
            return
        
        # 计算原始图片与显示图片的比例
        scale_x = self.bottom_image.width / img_width
        scale_y = self.bottom_image.height / img_height
        
        # 计算原始图片上的裁剪区域
        orig_x1 = int(rel_x1 * scale_x)
        orig_y1 = int(rel_y1 * scale_y)
        orig_x2 = int(rel_x2 * scale_x)
        orig_y2 = int(rel_y2 * scale_y)
        
        # 应用裁剪
        self.bottom_cropped = self.bottom_image.crop((orig_x1, orig_y1, orig_x2, orig_y2))
        
        # 确保比例为1:1
        size = min(self.bottom_cropped.width, self.bottom_cropped.height)
        left = (self.bottom_cropped.width - size) // 2
        top = (self.bottom_cropped.height - size) // 2
        self.bottom_cropped = self.bottom_cropped.crop((left, top, left + size, top + size))
        
        self.drawing_bottom = False
        self.bottom_canvas.delete("bottom_crop_rect")
        messagebox.showinfo("成功", "下方图裁剪完成")
    
    def stitch_images(self):
        if not self.top_cropped or not self.bottom_cropped:
            messagebox.showwarning("警告", "请先完成两张图片的裁剪")
            return
        
        # 计算输出宽度（取较小宽度）
        output_width = min(self.top_cropped.width, self.bottom_cropped.width)
        
        # 按比例调整上方图尺寸
        top_height = int(output_width / self.top_ratio)
        top_resized = self.top_cropped.resize((output_width, top_height), Image.Resampling.LANCZOS)
        
        # 按比例调整下方图尺寸
        bottom_resized = self.bottom_cropped.resize((output_width, output_width), Image.Resampling.LANCZOS)
        
        # 计算拼接后的总高度
        total_height = top_resized.height + bottom_resized.height
        
        # 创建新图片
        if self.bg_var.get() == "transparent":
            stitched = Image.new("RGBA", (output_width, total_height), (0, 0, 0, 0))
        else:
            stitched = Image.new("RGB", (output_width, total_height), "white")
        
        # 放置上方图（左对齐，实际上因为宽度相同就是完全对齐）
        stitched.paste(top_resized, (0, 0))
        
        # 放置下方图（水平居中，实际上因为宽度相同就是完全对齐）
        stitched.paste(bottom_resized, (0, top_resized.height))
        
        self.stitched_image = stitched
        self.update_stitch_preview()
        messagebox.showinfo("成功", "图片拼接完成")
    
    def save_image(self):
        if not self.stitched_image:
            messagebox.showwarning("警告", "没有可保存的图片")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="保存图片",
            defaultextension=".png",
            filetypes=[("PNG 图片", "*.png"), ("JPEG 图片", "*.jpg")]
        )
        
        if file_path:
            if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                # 如果是JPEG格式，需要转换为RGB模式
                if self.stitched_image.mode == 'RGBA':
                    rgb_image = Image.new('RGB', self.stitched_image.size, 'white')
                    rgb_image.paste(self.stitched_image, mask=self.stitched_image.split()[-1])
                    rgb_image.save(file_path, "JPEG")
                else:
                    self.stitched_image.save(file_path, "JPEG")
            else:
                self.stitched_image.save(file_path, "PNG")
            
            messagebox.showinfo("成功", f"图片已保存到: {file_path}")
    
    def on_window_resize(self, event):
        # 延迟更新，避免频繁重绘
        if hasattr(self, '_resize_id'):
            self.root.after_cancel(self._resize_id)
        self._resize_id = self.root.after(200, self._do_resize)
    
    def _do_resize(self):
        self.update_original_preview()
        self.update_stitch_preview()

    # ==================== 封面图提取工具 ====================
    def init_cover_extraction_tool(self):
        self.create_extraction_widgets()
    
    def create_extraction_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.extract_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="提取微信推送封面图", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        author_label = ttk.Label(main_frame, text="SoraKaGe_MeiOu", font=("Arial", 12))
        author_label.pack(pady=(0, 20))
        
        # 说明文字
        info_text = tk.Text(main_frame, height=6, width=80, wrap=tk.WORD, font=("Arial", 10))
        info_text.pack(pady=(0, 20), fill=tk.X)
        info_text.insert(tk.END, "使用说明：\n")
        info_text.insert(tk.END, "• 输入公众号文章链接，自动提取封面图\n")
        info_text.insert(tk.END, "• 提取的图片链接会自动复制到剪贴板\n")
        info_text.insert(tk.END, "• 图片会自动下载到当前用户桌面\n")
        info_text.insert(tk.END, "• 有bug联系QQ: Sorakagemo\n")
        info_text.insert(tk.END, "• 更新日期: 2025/11/19")
        info_text.config(state=tk.DISABLED)
        
        # 链接输入区域
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(url_frame, text="公众号链接:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame, width=60)
        self.url_entry.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Button(button_frame, text="提取封面图", 
                  command=self.extract_cover_image).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="清空", 
                  command=self.clear_url).pack(side=tk.LEFT)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="提取结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def extract_cover_image(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("警告", "请输入公众号链接")
            return
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "正在连接服务器...\n")
        self.root.update()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            self.result_text.insert(tk.END, f"连接失败，请检查网络或网址是否正确: {e}\n")
            return
        
        html = response.text
        
        # 方法1：尝试匹配 JS 中的 msg_cdn_url
        url_match = re.search(r'var\s+msg_cdn_url\s*=\s*"([^"]+)"', html)
        if url_match:
            image_url = url_match.group(1)
        else:
            # 方法2：尝试匹配 meta og:image 标签
            url_match = re.search(r'<meta property="og:image" content="(.*?)"', html)
            if url_match:
                image_url = url_match.group(1)
            else:
                self.result_text.insert(tk.END, "未找到封面图链接，请确认是公众号文章页\n")
                return
        
        self.result_text.insert(tk.END, f"找到封面图地址：{image_url}\n")
        
        # 复制到剪贴板
        try:
            pyperclip.copy(image_url)
            self.result_text.insert(tk.END, "图片链接已复制到剪贴板\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"复制到剪贴板失败: {e}\n")
        
        # 下载图片
        self.result_text.insert(tk.END, "正在下载图片...\n")
        self.root.update()
        
        try:
            file_path = self.save_image_from_url(image_url)
            self.result_text.insert(tk.END, f"图片已保存为: {file_path}\n")
            messagebox.showinfo("成功", f"封面图提取完成！\n图片已保存为: {file_path}")
        except Exception as e:
            self.result_text.insert(tk.END, f"下载图片时发生错误: {e}\n")
            messagebox.showerror("错误", f"下载图片失败: {e}")
    
    def save_image_from_url(self, image_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
        }
        response = requests.get(image_url, stream=True, headers=headers, timeout=10)
        if response.status_code == 200:
            desktop = Path.home() / "Desktop"
            if not desktop.exists():
                desktop = Path.home()
            
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"cover_{current_time}.jpg"
            file_path = desktop / file_name


            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            return str(file_path)
        else:
            raise Exception(f"服务器返回错误: {response.status_code}")
    
    def clear_url(self):
        self.url_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)

    # ==================== 图片压缩工具 ====================
    def init_image_compressor_tool(self):
        # 初始化压缩工具变量
        self.file_path = tk.StringVar()
        self.folder_path = tk.StringVar()
        self.quality = tk.IntVar(value=80)
        self.max_size_mb = tk.IntVar(value=10)
        self.include_subfolders = tk.BooleanVar(value=True)
        self.compression_in_progress = False
        self.png_strategy = tk.StringVar(value="auto")
        
        self.create_compressor_widgets()
    
    def create_compressor_widgets(self):
        main_frame = ttk.Frame(self.compress_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        title = ttk.Label(main_frame, text="压缩工具", font=('Arial', 16))
        title.grid(row=0, column=0, pady=(0, 10), sticky="n")
        
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        
        notebook.grid_rowconfigure(0, weight=1)
        notebook.grid_columnconfigure(0, weight=1)
        
        single_tab = ttk.Frame(notebook)
        notebook.add(single_tab, text="单文件压缩")
        self.create_single_tab(single_tab)
        
        batch_tab = ttk.Frame(notebook)
        notebook.add(batch_tab, text="批量压缩")
        self.create_batch_tab(batch_tab)
        
        settings_tab = ttk.Frame(notebook)
        notebook.add(settings_tab, text="设置")
        self.create_settings_tab(settings_tab)
    
    def create_single_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(parent, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="选择图片文件:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        file_frame = ttk.Frame(frame)
        file_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        file_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Entry(file_frame, textvariable=self.file_path, state='readonly').grid(row=0, column=0, sticky="ew")
        ttk.Button(file_frame, text="浏览...", command=self.select_file).grid(row=0, column=1, padx=(5, 0))
        
        ttk.Label(frame, text="压缩质量 (0-100):").grid(row=2, column=0, sticky="w", pady=(10, 5))
        
        quality_frame = ttk.Frame(frame)
        quality_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        quality_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Scale(quality_frame, from_=10, to=100, orient="horizontal", 
                 variable=self.quality).grid(row=0, column=0, sticky="ew")
        ttk.Label(quality_frame, textvariable=self.quality).grid(row=0, column=1, padx=5)
        
        ttk.Button(frame, text="压缩图片", command=self.compress_single, 
                  style="Accent.TButton").grid(row=4, column=0, pady=15)
        
        self.file_info = tk.Text(frame, height=6, width=40, state='disabled')
        self.file_info.grid(row=5, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.file_info.yview)
        scrollbar.grid(row=5, column=1, sticky="ns")
        self.file_info['yscrollcommand'] = scrollbar.set
        
        frame.grid_rowconfigure(5, weight=1)
    
    def create_batch_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(parent, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="选择图片文件夹:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        folder_frame = ttk.Frame(frame)
        folder_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        folder_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Entry(folder_frame, textvariable=self.folder_path, state='readonly').grid(row=0, column=0, sticky="ew")
        ttk.Button(folder_frame, text="浏览...", command=self.select_folder).grid(row=0, column=1, padx=(5, 0))
        
        ttk.Checkbutton(frame, text="包含子目录", variable=self.include_subfolders).grid(
            row=2, column=0, sticky="w", pady=(5, 10))
        
        ttk.Label(frame, text="压缩质量 (0-100):").grid(row=3, column=0, sticky="w", pady=(5, 5))
        
        quality_frame = ttk.Frame(frame)
        quality_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        quality_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Scale(quality_frame, from_=10, to=100, orient="horizontal", 
                 variable=self.quality).grid(row=0, column=0, sticky="ew")
        ttk.Label(quality_frame, textvariable=self.quality).grid(row=0, column=1, padx=5)
        
        ttk.Button(frame, text="开始批量压缩", command=self.compress_batch, 
                  style="Accent.TButton").grid(row=5, column=0, pady=15)
        
        self.progress = ttk.Progressbar(frame, orient="horizontal", mode='determinate')
        self.progress.grid(row=6, column=0, sticky="ew", pady=(0, 10))
        
        self.batch_info = tk.Text(frame, height=6, width=40, state='disabled')
        self.batch_info.grid(row=7, column=0, sticky="nsew")
        
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.batch_info.yview)
        scrollbar.grid(row=7, column=1, sticky="ns")
        self.batch_info['yscrollcommand'] = scrollbar.set
        
        frame.grid_rowconfigure(7, weight=1)
    
    def create_settings_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        
        frame = ttk.Frame(parent, padding="10")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(frame, text="最大文件大小 (MB):").grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        size_frame = ttk.Frame(frame)
        size_frame.grid(row=1, column=0, sticky="w", pady=(0, 20))
        ttk.Spinbox(size_frame, from_=1, to=100, textvariable=self.max_size_mb, width=5).grid(row=0, column=0)
        ttk.Label(size_frame, text="MB").grid(row=0, column=1, padx=5)
        
        ttk.Label(frame, text="PNG转换策略:").grid(row=2, column=0, sticky="w", pady=(10, 5))
        
        ttk.Radiobutton(frame, text="自动转为JPEG (压缩率更高)", 
                       variable=self.png_strategy, value="auto").grid(row=3, column=0, sticky="w")
        ttk.Radiobutton(frame, text="保持PNG格式 (保留透明度)", 
                       variable=self.png_strategy, value="keep").grid(row=4, column=0, sticky="w", pady=(0, 20))
        
        ttk.Button(frame, text="恢复默认设置", command=self.reset_settings).grid(row=5, column=0)
    
    def reset_settings(self):
        self.quality.set(85)
        self.max_size_mb.set(10)
        self.png_strategy.set("auto")
        messagebox.showinfo("提示", "已恢复默认设置")
        self.status_var.set("已恢复默认设置")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="选择要压缩的图片",
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        
        if file_path:
            self.file_path.set(file_path)
            self.update_file_info(file_path)
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择包含图片的文件夹")
        if folder_path:
            self.folder_path.set(folder_path)
            self.status_var.set(f"已选择文件夹: {folder_path}")
    
    def update_file_info(self, file_path):
        try:
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            with Image.open(file_path) as img:
                width, height = img.size
                format = img.format
            
            info_text = (
                f"文件名: {os.path.basename(file_path)}\n"
                f"大小: {file_size:.2f} MB\n"
                f"尺寸: {width} x {height}\n"
                f"格式: {format}\n"
                f"路径: {file_path}"
            )
            
            self.file_info.config(state='normal')
            self.file_info.delete(1.0, tk.END)
            self.file_info.insert(tk.END, info_text)
            self.file_info.config(state='disabled')
            
            if file_size < self.max_size_mb.get():
                self.status_var.set(f"提示: 文件已小于{self.max_size_mb.get()}MB，无需压缩")
            else:
                self.status_var.set("已选择文件，可以开始压缩")
        except Exception as e:
            self.status_var.set(f"更新文件信息失败: {str(e)}")
            self.set_error_status(f"更新文件信息失败: {str(e)}")
    
    def compress_single(self):
        if self.compression_in_progress:
            return
        
        input_path = self.file_path.get()
        if not input_path:
            messagebox.showerror("错误", "请先选择图片文件")
            self.set_error_status("请先选择图片文件")
            return
        
        try:
            original_size = os.path.getsize(input_path) / (1024 * 1024)
            if original_size < self.max_size_mb.get():
                messagebox.showinfo("提示", f"原始文件已经小于{self.max_size_mb.get()}MB，无需压缩")
                self.status_var.set(f"提示: 原始文件已小于{self.max_size_mb.get()}MB")
                return
            
            directory, filename = os.path.split(input_path)
            name, ext = os.path.splitext(filename)
            output_filename = f"{name}_compressed_q{self.quality.get()}{ext}"
            output_path = os.path.join(directory, output_filename)
            
            self.compression_in_progress = True
            success, final_quality = self.compress_image(input_path, output_path, self.quality.get())
            self.compression_in_progress = False
            
            if success:
                compressed_size = os.path.getsize(output_path) / (1024 * 1024)
                message = (
                    f"图片压缩成功!\n\n"
                    f"原始大小: {original_size:.2f} MB\n"
                    f"压缩后大小: {compressed_size:.2f} MB\n"
                    f"最终质量: {final_quality}\n\n"
                    f"保存在: {output_path}"
                )
                messagebox.showinfo("完成", message)
                self.status_var.set(f"压缩完成! 最终质量: {final_quality}")
                self.update_file_info(output_path)
            else:
                messagebox.showerror("压缩失败", f"图片压缩过程中出现错误")
                self.set_error_status("图片压缩过程中出现错误")
        except Exception as e:
            messagebox.showerror("错误", f"压缩过程中发生错误: {str(e)}")
            self.compression_in_progress = False
            self.set_error_status(f"压缩错误: {str(e)}")
    
    def compress_batch(self):
        if self.compression_in_progress:
            return
        
        folder_path = self.folder_path.get()
        if not folder_path:
            messagebox.showerror("错误", "请先选择图片文件夹")
            self.set_error_status("请先选择图片文件夹")
            return
        
        try:
            image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
            image_files = []
            
            if self.include_subfolders.get():
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        if file.lower().endswith(image_extensions):
                            image_files.append(os.path.join(root, file))
            else:
                for file in os.listdir(folder_path):
                    if file.lower().endswith(image_extensions):
                        image_files.append(os.path.join(folder_path, file))
            
            if not image_files:
                messagebox.showerror("错误", "选择的文件夹中没有找到图片文件")
                self.set_error_status("文件夹中没有找到图片文件")
                return
            
            confirm = messagebox.askyesno("确认", f"找到 {len(image_files)} 张图片，是否开始批量压缩?")
            if not confirm:
                return
            
            self.compression_in_progress = True
            self.progress['maximum'] = len(image_files)
            self.progress['value'] = 0
            
            total_original_size = 0
            total_compressed_size = 0
            success_count = 0
            skip_count = 0
            
            for i, input_path in enumerate(image_files):
                self.root.update()
                self.status_var.set(f"正在处理: {os.path.basename(input_path)} ({i+1}/{len(image_files)})")
                
                try:
                    original_size = os.path.getsize(input_path) / (1024 * 1024)
                    total_original_size += original_size
                    
                    if original_size < self.max_size_mb.get():
                        skip_count += 1
                    else:
                        directory, filename = os.path.split(input_path)
                        name, ext = os.path.splitext(filename)
                        output_filename = f"{name}_compressed_q{self.quality.get()}{ext}"
                        output_path = os.path.join(directory, output_filename)
                        
                        success, final_quality = self.compress_image(input_path, output_path, self.quality.get())
                        
                        if success:
                            compressed_size = os.path.getsize(output_path) / (1024 * 1024)
                            total_compressed_size += compressed_size
                            success_count += 1
                    
                    self.progress['value'] = i + 1
                except Exception as e:
                    self.status_var.set(f"处理 {os.path.basename(input_path)} 时出错: {str(e)}")
                    self.set_error_status(f"处理图片出错: {str(e)}")
            
            self.compression_in_progress = False
            self.status_var.set(f"批量压缩完成! 成功: {success_count}, 跳过: {skip_count}")
            
            info_text = (
                f"处理完成!\n\n"
                f"总图片数: {len(image_files)}\n"
                f"成功压缩: {success_count}\n"
                f"跳过(已小于{self.max_size_mb.get()}MB): {skip_count}\n\n"
                f"原始总大小: {total_original_size:.2f} MB\n"
                f"压缩后总大小: {total_compressed_size:.2f} MB\n"
                f"节省空间: {total_original_size - total_compressed_size:.2f} MB"
            )
            
            self.batch_info.config(state='normal')
            self.batch_info.delete(1.0, tk.END)
            self.batch_info.insert(tk.END, info_text)
            self.batch_info.config(state='disabled')
            
            messagebox.showinfo("完成", f"批量压缩完成!\n\n成功压缩 {success_count} 张图片\n跳过 {skip_count} 张已小于{self.max_size_mb.get()}MB的图片")
        except Exception as e:
            messagebox.showerror("错误", f"批量压缩过程中发生错误: {str(e)}")
            self.compression_in_progress = False
            self.set_error_status(f"批量压缩错误: {str(e)}")
    
    def compress_image(self, input_path, output_path, quality):
        max_size_bytes = self.max_size_mb.get() * 1024 * 1024
        
        try:
            with Image.open(input_path) as img:
                original_format = img.format
                file_base, file_ext = os.path.splitext(output_path)
                
                if original_format in ('PNG', 'GIF') and self.png_strategy.get() == "auto":
                    img = img.convert('RGB')
                    output_path = f"{file_base}.jpg"
                    output_format = 'JPEG'
                else:
                    output_format = original_format
                
                with io.BytesIO() as buffer:
                    img.save(buffer, format=output_format, quality=quality, optimize=True)
                    buffer_size = buffer.tell()
                    
                    if buffer_size <= max_size_bytes:
                        with open(output_path, 'wb') as f:
                            f.write(buffer.getvalue())
                        return True, quality
                
                for q in range(quality - 5, 10, -5):
                    with io.BytesIO() as buffer:
                        img.save(buffer, format=output_format, quality=q, optimize=True)
                        buffer_size = buffer.tell()
                        
                        if buffer_size <= max_size_bytes:
                            with open(output_path, 'wb') as f:
                                f.write(buffer.getvalue())
                            return True, q
                
                temp_img = img.copy()
                adjusted_quality = max(quality, 70)
                
                while True:
                    new_width = int(temp_img.width * 0.9)
                    new_height = int(temp_img.height * 0.9)
                    temp_img = temp_img.resize((new_width, new_height), Image.LANCZOS)
                    
                    with io.BytesIO() as buffer:
                        temp_img.save(buffer, format=output_format, quality=adjusted_quality, optimize=True)
                        buffer_size = buffer.tell()
                        
                        if buffer_size <= max_size_bytes:
                            with open(output_path, 'wb') as f:
                                f.write(buffer.getvalue())
                            return True, adjusted_quality
                    
                    if new_width < 100 or new_height < 100:
                        self.status_var.set(f"无法将 {os.path.basename(input_path)} 压缩到指定大小")
                        return False, quality
        
        except Exception as e:
            self.status_var.set(f"处理 {os.path.basename(input_path)} 时出错: {str(e)}")
            return False, quality

if __name__ == "__main__":
    root = tk.Tk()
    app = WeChatTools(root)
    root.mainloop()
