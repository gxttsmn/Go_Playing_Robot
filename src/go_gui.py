import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from go_ai import GoAI

class GoGameGUI:
    """围棋游戏图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("围棋博弈机器人 - ModelScope + Qwen")
        self.root.geometry("1200x800")
        
        # 初始化AI
        try:
            self.go_ai = GoAI()
            self.ai_status = "已连接"
        except Exception as e:
            messagebox.showerror("错误", f"AI初始化失败：{str(e)}")
            self.ai_status = "连接失败"
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧棋盘区域
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 棋盘标题
        board_title = ttk.Label(left_frame, text="围棋棋盘", font=("Arial", 16, "bold"))
        board_title.pack(pady=(0, 10))
        
        # 棋盘画布
        self.canvas = tk.Canvas(left_frame, width=600, height=600, bg="#DEB887")
        self.canvas.pack()
        
        # 棋盘控制按钮
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="获取AI建议", command=self.get_ai_suggestion).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="重置游戏", command=self.reset_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="分析局面", command=self.analyze_position).pack(side=tk.LEFT, padx=5)
        
        # AI自动响应开关
        self.auto_ai = tk.BooleanVar(value=True)
        ttk.Checkbutton(button_frame, text="AI自动响应", variable=self.auto_ai).pack(side=tk.LEFT, padx=10)
        
        # 右侧信息区域
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # AI状态
        status_frame = ttk.LabelFrame(right_frame, text="AI状态")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text=f"ModelScope Qwen: {self.ai_status}")
        self.status_label.pack(pady=5)
        
        # 游戏信息
        info_frame = ttk.LabelFrame(right_frame, text="游戏信息")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_text = tk.Text(info_frame, height=8, wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # AI分析结果 - 精简版
        analysis_frame = ttk.LabelFrame(right_frame, text="AI分析结果")
        analysis_frame.pack(fill=tk.BOTH, expand=True)
        
        self.analysis_text = scrolledtext.ScrolledText(analysis_frame, wrap=tk.WORD, height=8)
        self.analysis_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 当前操作者标识区域
        current_player_frame = ttk.LabelFrame(right_frame, text="当前操作者")
        current_player_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.current_player_label = ttk.Label(current_player_frame, text="用户(黑棋)", 
                                            font=("Arial", 14, "bold"), 
                                            foreground="red")
        self.current_player_label.pack(pady=10)
        
        # 绘制棋盘
        self.draw_board()
        self.update_info()
        
        # 绑定鼠标点击事件
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
    def draw_board(self):
        """绘制围棋棋盘"""
        self.canvas.delete("all")
        
        # 棋盘参数
        board_size = 19
        cell_size = 30
        start_x = 30
        start_y = 30
        
        # 绘制网格线
        for i in range(board_size):
            # 垂直线
            x = start_x + i * cell_size
            self.canvas.create_line(x, start_y, x, start_y + (board_size-1) * cell_size, fill="black", width=1)
            
            # 水平线
            y = start_y + i * cell_size
            self.canvas.create_line(start_x, y, start_x + (board_size-1) * cell_size, y, fill="black", width=1)
        
        # 绘制星位
        star_positions = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
        for row, col in star_positions:
            x = start_x + col * cell_size
            y = start_y + row * cell_size
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
        
        # 绘制棋子
        for row in range(board_size):
            for col in range(board_size):
                if self.go_ai.board[row, col] != 0:
                    x = start_x + col * cell_size
                    y = start_y + row * cell_size
                    color = "black" if self.go_ai.board[row, col] == 1 else "white"
                    self.canvas.create_oval(x-12, y-12, x+12, y+12, fill=color, outline="black", width=2)
        
        # 高亮最新棋子
        self.highlight_latest_moves()
        
        # 存储棋盘参数供点击事件使用
        self.cell_size = cell_size
        self.start_x = start_x
        self.start_y = start_y
        
    def highlight_latest_moves(self):
        """高亮最新棋子 - 只高亮最新一步"""
        if len(self.go_ai.move_history) < 1:
            return
            
        # 获取最新一步棋
        latest_move = self.go_ai.move_history[-1]
        row, col, player = latest_move
        
        x = self.start_x + col * self.cell_size
        y = self.start_y + row * self.cell_size
        
        # 根据玩家选择高亮颜色
        if player == 1:  # 用户(黑棋) - 使用红色系
            highlight_colors = ["#FF6B6B", "#FF8E8E", "#FFB1B1", "#FFD4D4"]
        else:  # AI(白棋) - 使用蓝色系
            highlight_colors = ["#4ECDC4", "#7EDDD6", "#A8E6E1", "#C2F0EB"]
        
        # 绘制多层高亮效果，创建渐进效果
        for j, color in enumerate(highlight_colors):
            radius = 15 + j * 2  # 逐渐增大的半径
            width = 3 - j * 0.5  # 逐渐减小的线宽
            if width < 1:
                width = 1
            self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                                  outline=color, width=width, fill="")
        
    def on_canvas_click(self, event):
        """处理棋盘点击事件 - 添加权限控制"""
        if self.ai_status != "已连接":
            messagebox.showwarning("警告", "AI未连接，无法下棋")
            return
        
        # 权限控制：只有轮到用户(黑棋)时才能点击下棋
        if self.go_ai.current_player != 1:
            messagebox.showinfo("提示", "当前轮到AI(白棋)下棋，请等待AI思考...")
            return
            
        # 计算点击的格子坐标
        col = round((event.x - self.start_x) / self.cell_size)
        row = round((event.y - self.start_y) / self.cell_size)
        
        # 检查坐标是否有效
        if 0 <= row < 19 and 0 <= col < 19:
            if self.go_ai.make_move(row, col):
                self.draw_board()
                self.update_info()
                self.analysis_text.insert(tk.END, f"用户下棋：({row+1}, {col+1})\n")
                self.analysis_text.see(tk.END)
                
                # 如果开启自动AI响应，让AI下棋
                if self.auto_ai.get() and self.go_ai.current_player == -1:  # 轮到AI(白棋)
                    self.analysis_text.insert(tk.END, "AI正在思考...\n")
                    self.analysis_text.see(tk.END)
                    self.root.update()
                    
                    # 启动AI思考线程
                    self.go_ai.get_ai_move(self.on_ai_move_complete)
            else:
                messagebox.showwarning("警告", "该位置已有棋子或无效位置")
                
    def on_ai_move_complete(self, row, col, suggestion):
        """AI下棋完成回调 - 需要在主线程中执行"""
        # 使用after方法确保在主线程中执行GUI更新
        self.root.after(0, lambda: self._update_ai_result(row, col, suggestion))
        
    def _update_ai_result(self, row, col, suggestion):
        """更新AI结果的内部方法 - 精简版"""
        if row is not None and col is not None:
            # AI成功下棋
            self.draw_board()
            self.update_info()
            self.analysis_text.insert(tk.END, f"AI下棋：({row+1}, {col+1})\n")
            
            # 精简AI分析结果，只显示关键信息
            simplified_analysis = self.simplify_ai_analysis(suggestion)
            self.analysis_text.insert(tk.END, f"AI分析：{simplified_analysis}\n\n")
            self.analysis_text.see(tk.END)
        else:
            # AI只给出建议，没有下棋
            simplified_analysis = self.simplify_ai_analysis(suggestion)
            self.analysis_text.insert(tk.END, f"AI建议：{simplified_analysis}\n\n")
            self.analysis_text.see(tk.END)
    
    def simplify_ai_analysis(self, analysis):
        """精简AI分析结果"""
        # 提取关键信息，限制长度
        lines = analysis.split("\\n")
        key_lines = []
        
        for line in lines:
            line = line.strip()
            if any(keyword in line for keyword in ["推荐", "建议", "坐标", "下在", "选择", "位置"]):
                key_lines.append(line)
            elif len(line) < 50 and any(keyword in line for keyword in ["优势", "劣势", "策略", "应对"]):
                key_lines.append(line)
        
        # 如果找到关键信息，返回前3行
        if key_lines:
            return "\\n".join(key_lines[:3])
        else:
            # 如果没有找到关键信息，返回前100个字符
            return analysis[:100] + "..." if len(analysis) > 100 else analysis
                
    def get_ai_suggestion(self):
        """获取AI建议"""
        if self.ai_status != "已连接":
            messagebox.showwarning("警告", "AI未连接")
            return
            
        self.analysis_text.insert(tk.END, "正在获取AI建议...\n")
        self.analysis_text.see(tk.END)
        self.root.update()
        
        try:
            suggestion = self.go_ai.get_ai_suggestion()
            simplified_analysis = self.simplify_ai_analysis(suggestion)
            self.analysis_text.insert(tk.END, f"AI建议：{simplified_analysis}\n\n")
            self.analysis_text.see(tk.END)
        except Exception as e:
            self.analysis_text.insert(tk.END, f"获取AI建议失败：{str(e)}\n\n")
            self.analysis_text.see(tk.END)
            
    def analyze_position(self):
        """分析当前局面"""
        if self.ai_status != "已连接":
            messagebox.showwarning("警告", "AI未连接")
            return
            
        self.analysis_text.insert(tk.END, "正在分析局面...\n")
        self.analysis_text.see(tk.END)
        self.root.update()
        
        try:
            analysis = self.go_ai.analyze_position("请详细分析当前局面。")
            simplified_analysis = self.simplify_ai_analysis(analysis)
            self.analysis_text.insert(tk.END, f"局面分析：{simplified_analysis}\n\n")
            self.analysis_text.see(tk.END)
        except Exception as e:
            self.analysis_text.insert(tk.END, f"分析失败：{str(e)}\n\n")
            self.analysis_text.see(tk.END)
            
    def reset_game(self):
        """重置游戏"""
        self.go_ai.reset_game()
        self.draw_board()
        self.update_info()
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, "游戏已重置\n")
        
    def update_info(self):
        """更新游戏信息"""
        self.info_text.delete(1.0, tk.END)
        
        # 明确显示当前玩家角色
        current_player_name = "用户(黑棋)" if self.go_ai.current_player == 1 else "AI(白棋)"
        
        info = f"""已下步数：{len(self.go_ai.move_history)}
棋盘大小：{self.go_ai.board_size}x{self.go_ai.board_size}

最近几步：
"""
        if self.go_ai.move_history:
            for i, (row, col, player) in enumerate(self.go_ai.move_history[-5:]):
                player_name = "用户(黑棋)" if player == 1 else "AI(白棋)"
                info += f"第{i+1}步：{player_name} ({row+1}, {col+1})\n"
        else:
            info += "暂无棋子"
            
        self.info_text.insert(tk.END, info)
        
        # 更新当前操作者标识
        self.update_current_player_display()
        
    def update_current_player_display(self):
        """更新当前操作者显示"""
        if self.go_ai.current_player == 1:  # 用户(黑棋)
            self.current_player_label.config(text="用户(黑棋)", foreground="red")
        else:  # AI(白棋)
            self.current_player_label.config(text="AI(白棋)", foreground="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = GoGameGUI(root)
    root.mainloop()
