# 🌈 Nyan Cat Progress Bar

一个马赛克风格的彩虹小猫时间进度条，固定在 Mac 屏幕底部 Dock 上方。

小猫的位置代表当天的时间进度：
- **0:00** → 屏幕最左边
- **24:00** → 屏幕最右边
- 实时移动，带彩虹拖尾和像素动画

## ✨ 功能

- 🐱 像素风 Nyan Cat（Pop-Tart 饼干猫身 + 两帧腿部动画）
- 🌈 6色彩虹拖尾，带颜色流动和闪烁星点
- 📍 小猫位置 = 当天时间进度，每秒更新
- 🔧 S/M/L 三档大小可调
- 💬 时间气泡（显示时间 + 进度百分比 + 迷你进度条）
- 🚀 开机自启动（macOS LaunchAgent）
- 📦 系统托盘图标

## 🚀 快速开始

### 安装依赖

```bash
pip install PySide6
```

### 运行

```bash
python main.py                 # 默认中号
python main.py --size large    # 大号
python main.py --size small    # 小号
python main.py --hide-bubble   # 隐藏时间气泡
```

### 打包为 .app

```bash
# 方式1：py2app
pip install py2app
python setup.py py2app

# 方式2：pyinstaller
pip install pyinstaller
pyinstaller --noconfirm --windowed --name "NyanCatProgressBar" main.py
```

## 🌐 Web 预览

打开 `web-preview/index.html` 可以在浏览器中预览效果。

## 📁 项目结构

```
nyan-cat-progress-bar/
├── main.py           # 主程序
├── config.py         # 像素画数据、颜色、常量
├── setup.py          # py2app 打包配置
├── Makefile          # 快捷命令
├── requirements.txt  # Python 依赖
├── web-preview/      # 浏览器预览版
│   └── index.html
└── README.md
```

## 📝 License

MIT
