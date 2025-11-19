#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
围棋博弈机器人主程序
使用ModelScope的Qwen模型进行围棋对弈和分析
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from go_gui import GoGameGUI
import tkinter as tk

def main():
    """主函数"""
    print("=" * 50)
    print("围棋博弈机器人 - ModelScope + Qwen")
    print("=" * 50)
    print("正在启动图形界面...")
    
    try:
        root = tk.Tk()
        app = GoGameGUI(root)
        print("界面启动成功！")
        print("使用说明：")
        print("1. 点击棋盘下棋")
        print("2. 使用获取AI建议按钮获取AI建议")
        print("3. 使用分析局面按钮分析当前局面")
        print("4. 使用重置游戏按钮重新开始")
        print("=" * 50)
        root.mainloop()
    except Exception as e:
        print(f"启动失败：{str(e)}")
        print("请检查依赖包是否正确安装")

if __name__ == "__main__":
    main()
