# style-distill · 参考视频风格蒸馏

给一条参考视频（抖音 / B 站 / YouTube 链接或本地 mp4），把它的**画面语法**蒸馏成可复用的风格配方，再用代码（Remotion 或 Playwright 引擎）做出同风格的原创作品。

合并自两个开源工程的风格蒸馏能力：
- [Azure12355/weilanx-claude-videos](https://github.com/Azure12355/weilanx-claude-videos)：机器拆解报告、色板 / 强调色、运动强度、音频卡点、动效切片、风格配方卡、Remotion 素材包与对照自查
- [alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion)：逐帧灰度差找切点、转场接触表、运动热图、BPM 节拍网格拟合、速通类五层机制、跨场景风格提炼、并排对照与状态分级

## 目录
- `SKILL.md`：完整流程（给 AI 编程助手读）
- `scripts/`：`fetch_douyin.py` 抖音无水印下载、`fetch_reference.py` 通用下载、`analyze.py` 镜头/色板/运动报告、`breakdown.py` 切点与转场拆解、`strip.py` 动效切片、`beats.py` 节拍网格、`side_by_side.py` 并排对照
- `references/`：拆解方法、机制分析、节奏配乐、跨场景提炼、配方卡模板

## 快速开始
```sh
uv run scripts/fetch_douyin.py "https://v.douyin.com/xxxx/" --out ref
uv run --with numpy --with pillow python scripts/analyze.py ref/video.mp4 --out 报告
uv run scripts/breakdown.py --video ref/video.mp4 --out 拆解
```

## 原则
学画面语法（色彩、版式、转场、缓动、节奏、叙事机制），不搬内容（文案、分镜、人设、水印、配乐）。

## 许可
MIT。原工程许可见 `licenses/`。
