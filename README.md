# 围棋博弈机器人 - ModelScope + Qwen

## 项目简介

这是一个基于ModelScope平台和通义千问(Qwen)大模型的围棋博弈机器人项目。通过AI模型分析围棋局面，为用户提供专业的围棋建议和策略分析。

## 功能特点

-  **AI棋局分析**: 使用Qwen模型分析当前围棋局面
-  **智能建议**: 获取AI推荐的最佳下法
-  **图形界面**: 直观的19x19围棋棋盘界面
-  **实时信息**: 显示当前玩家、步数、历史记录
-  **多种操作**: 支持鼠标点击和手动输入坐标下棋

## 技术栈

- **AI模型**: ModelScope Qwen-Plus
- **编程语言**: Python 3.7+
- **图形界面**: Tkinter
- **数据处理**: NumPy
- **API调用**: DashScope SDK

## 安装说明

### 1. 克隆项目
```bash
git clone <项目地址>
cd Go_Playing_Robot
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置API密钥
在项目根目录创建`.env`文件，添加您的ModelScope API密钥：
```
DASHSCOPE_API_KEY=your_api_key_here
```

## 使用方法

### 启动程序
```bash
python main.py
```

### 操作说明

1. **下棋**: 直接点击棋盘上的交叉点下棋
2. **获取AI建议**: 点击"获取AI建议"按钮，AI会分析当前局面并给出建议
3. **分析局面**: 点击"分析局面"按钮，获取详细的局面分析
4. **手动下棋**: 在右侧输入框中输入坐标(行,列)进行下棋
5. **重置游戏**: 点击"重置游戏"按钮重新开始

## 项目结构

```
Go_Playing_Robot/
 src/
    go_ai.py          # 围棋AI核心逻辑
    go_gui.py         # 图形用户界面
 main.py               # 主程序入口
 requirements.txt      # 项目依赖
 .env                  # 环境变量配置
 README.md            # 项目说明
```

## API配置

### 获取ModelScope API密钥

1. 访问 [ModelScope官网](https://modelscope.cn/)
2. 注册并登录账号
3. 进入控制台，获取API密钥
4. 将密钥配置到`.env`文件中

### 支持的模型

- **qwen-plus**: 推荐使用，平衡性能和成本
- **qwen-max**: 最强性能，适合复杂分析
- **qwen-turbo**: 快速响应，适合实时对弈

## 注意事项

1. 确保网络连接正常，API调用需要访问ModelScope服务
2. 首次使用可能需要等待模型加载
3. API调用会产生费用，请注意使用量
4. 建议在稳定的网络环境下使用

## 故障排除

### 常见问题

1. **API密钥错误**: 检查`.env`文件中的密钥是否正确
2. **网络连接失败**: 检查网络连接和防火墙设置
3. **依赖包缺失**: 运行`pip install -r requirements.txt`安装依赖
4. **界面显示异常**: 检查Python版本和Tkinter支持

### 错误代码

- `API调用失败`: 检查API密钥和网络连接
- `AI初始化失败`: 检查环境变量配置
- `坐标无效`: 确保输入的坐标在1-19范围内

## 开发计划

- [ ] 添加棋谱保存和加载功能
- [ ] 支持不同棋盘大小(9x9, 13x13)
- [ ] 集成更多AI模型选择
- [ ] 添加对弈记录和统计
- [ ] 优化AI分析算法

## 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件至项目维护者

---

**享受围棋的乐趣，与AI一起探索围棋的奥秘！** 
