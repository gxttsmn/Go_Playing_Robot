import os
import numpy as np
from dotenv import load_dotenv
from dashscope import Generation
import json
import threading
import time
import re

# Load environment variables
load_dotenv()

class GoAI:
    """围棋AI类，使用ModelScope的Qwen模型进行棋局分析"""
    
    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY not found in environment variables")
        
        # 围棋棋盘状态
        self.board_size = 19
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1  # 1 for black (用户), -1 for white (AI)
        self.move_history = []
        self.ai_thinking = False
        
    def get_board_state_description(self):
        """将棋盘状态转换为文字描述"""
        description = "当前棋盘状态：\n"
        description += f"棋盘大小：{self.board_size}x{self.board_size}\n"
        player_name = "用户(黑棋)" if self.current_player == 1 else "AI(白棋)"
        description += f"当前玩家：{player_name}\n"
        description += f"已下步数：{len(self.move_history)}\n\n"
        
        # 描述已占用的位置
        if self.move_history:
            description += "已占用的位置：\n"
            for i, (row, col, player) in enumerate(self.move_history):
                player_name = "用户(黑棋)" if player == 1 else "AI(白棋)"
                description += f"第{i+1}步：{player_name} 下在 ({row+1}, {col+1})\n"
        
        return description
    
    def analyze_position(self, prompt_addition=""):
        """使用Qwen模型分析当前棋局"""
        if self.ai_thinking:
            return "AI正在思考中，请稍候..."
            
        self.ai_thinking = True
        try:
            base_prompt = f"""你是一个专业的围棋AI助手。请分析当前的围棋局面并给出建议。

{self.get_board_state_description()}

请从以下角度分析：
1. 当前局面的优劣
2. 推荐的最佳下法（给出坐标）
3. 分析对手可能的应对
4. 整体战略建议

{prompt_addition}

请用中文回答，并给出具体的坐标建议（格式：行,列，从1开始计数）。"""

            response = Generation.call(
                model="qwen-plus",
                prompt=base_prompt,
                api_key=self.api_key,
                max_tokens=1000,
                temperature=0.7
            )
            
            if response.status_code == 200:
                return response.output.text
            else:
                return f"API调用失败：{response.message}"
                
        except Exception as e:
            return f"分析过程中出现错误：{str(e)}"
        finally:
            self.ai_thinking = False
    
    def make_move(self, row, col):
        """在指定位置下棋"""
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            if self.board[row, col] == 0:  # 空位
                self.board[row, col] = self.current_player
                self.move_history.append((row, col, self.current_player))
                self.current_player *= -1  # 切换玩家
                return True
        return False
    
    def get_ai_suggestion(self):
        """获取AI建议的下一步棋"""
        analysis = self.analyze_position("请给出具体的下一步建议坐标。")
        return analysis
    
    def extract_coordinates(self, text):
        """从AI回复中提取坐标"""
        # 多种坐标格式的正则表达式
        patterns = [
            r"(\d+)[,，]\s*(\d+)",  # 数字,数字
            r"(\d+)\s*[,，]\s*(\d+)",  # 数字 , 数字
            r"(\d+)\s+(\d+)",  # 数字 数字
            r"(\d+)-(\d+)",  # 数字-数字
            r"(\d+)\.(\d+)",  # 数字.数字
            r"(\d+)\s*行\s*(\d+)\s*列",  # 数字行数字列
            r"(\d+)\s*列\s*(\d+)\s*行",  # 数字列数字行
            r"(\d+)\s*,\s*(\d+)",  # 数字, 数字
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                try:
                    row, col = int(matches[0][0]), int(matches[0][1])
                    # 检查坐标是否在有效范围内
                    if 1 <= row <= 19 and 1 <= col <= 19:
                        return row - 1, col - 1  # 转换为0索引
                except ValueError:
                    continue
        
        return None, None
    
    def get_quick_ai_move(self, callback=None):
        """快速获取AI的下一步棋 - 优化版本"""
        def ai_think():
            try:
                # 使用更简洁的提示词，减少token消耗
                quick_prompt = f"""围棋局面分析：
{self.get_board_state_description()}

请快速给出下一步建议坐标，格式：行,列（1-19）。选择空位下棋。"""
                
                response = Generation.call(
                    model="qwen-plus",
                    prompt=quick_prompt,
                    api_key=self.api_key,
                    max_tokens=300,  # 减少token数量
                    temperature=0.5  # 降低随机性，提高响应速度
                )
                
                if response.status_code != 200:
                    if callback:
                        callback(None, None, f"API调用失败：{response.message}")
                    return False
                
                suggestion = response.output.text
                print(f"AI快速回复: {suggestion[:100]}...")
                
                # 尝试从建议中提取坐标
                row, col = self.extract_coordinates(suggestion)
                
                if row is not None and col is not None:
                    print(f"提取到坐标: ({row+1}, {col+1})")
                    
                    if 0 <= row < 19 and 0 <= col < 19 and self.board[row, col] == 0:
                        # 下棋
                        self.board[row, col] = self.current_player
                        self.move_history.append((row, col, self.current_player))
                        self.current_player *= -1
                        
                        print(f"AI成功下棋: ({row+1}, {col+1})")
                        
                        if callback:
                            callback(row, col, suggestion)
                        return True
                    else:
                        print(f"坐标无效或位置已有棋子: ({row+1}, {col+1})")
                
                # 如果坐标无效，使用智能备用位置
                fallback_positions = self.get_smart_fallback_positions()
                for fallback_row, fallback_col in fallback_positions:
                    if self.board[fallback_row, fallback_col] == 0:
                        self.board[fallback_row, fallback_col] = self.current_player
                        self.move_history.append((fallback_row, fallback_col, self.current_player))
                        self.current_player *= -1
                        print(f"AI使用智能备用位置下棋: ({fallback_row+1}, {fallback_col+1})")
                        if callback:
                            callback(fallback_row, fallback_col, f"AI选择备用位置: ({fallback_row+1}, {fallback_col+1})")
                        return True
                
                # 如果没有找到有效坐标，返回建议
                if callback:
                    callback(None, None, suggestion)
                return False
                
            except Exception as e:
                print(f"AI思考出错: {str(e)}")
                if callback:
                    callback(None, None, f"AI思考出错：{str(e)}")
                return False
        
        # 在后台线程中运行AI思考
        thread = threading.Thread(target=ai_think)
        thread.daemon = True
        thread.start()
        return thread
    
    def get_smart_fallback_positions(self):
        """获取智能备用位置"""
        # 根据当前局面智能选择备用位置
        occupied_positions = [(row, col) for row, col, _ in self.move_history]
        
        # 优先选择星位
        star_positions = [(3, 3), (3, 9), (3, 15), (9, 3), (9, 9), (9, 15), (15, 3), (15, 9), (15, 15)]
        for pos in star_positions:
            if pos not in occupied_positions:
                yield pos
        
        # 然后选择小目
        small_eye_positions = [(3, 4), (4, 3), (3, 16), (4, 17), (16, 3), (17, 4), (16, 17), (17, 16)]
        for pos in small_eye_positions:
            if pos not in occupied_positions:
                yield pos
        
        # 最后选择其他常见位置
        other_positions = [(2, 2), (2, 16), (16, 2), (16, 16), (10, 10), (5, 5), (5, 15), (15, 5), (15, 15)]
        for pos in other_positions:
            if pos not in occupied_positions:
                yield pos
    
    def get_ai_move(self, callback=None):
        """获取AI的下一步棋并自动下棋 - 使用快速版本"""
        return self.get_quick_ai_move(callback)
    
    def reset_game(self):
        """重置游戏"""
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.current_player = 1
        self.move_history = []
        self.ai_thinking = False

if __name__ == "__main__":
    # 测试AI功能
    ai = GoAI()
    print("围棋AI初始化成功！")
    print("测试分析功能...")
    analysis = ai.analyze_position("请分析开局阶段的最佳策略。")
    print("AI分析结果：")
    print(analysis)

