# style-distill · 参考视频 → 风格配方（合并版）

合并自两个 MIT 项目的「风格蒸馏」部分（许可见 `licenses/`）：
- weilanx-claude-videos 的 `weilanx-creator-distill-video`：机器拆解报告、动效切片、配方卡、Remotion 素材包、对照自查。
- huashu-art-motion 的 01 拆解 / 02 机制 / 05 节奏 / 15 跨场景提炼 / 16 并排对照：逐帧差找转场、节拍网格拟合、运动热图、跨作品提炼、状态诚实。

本目录：`/workspace/skills/style-distill`（下文 `$SD`）。脚本都在 `$SD/scripts/`，参考文档在 `$SD/references/`。

## 边界：风格一比一，内容不搬
- **学**：配色体系、字体气质与层级、版式网格、入场/退场/转场、缓动和帧数、镜头运动、节奏（切点频率、镜头长度、卡点）、道具/图表画法、质感（颗粒、光晕、纸纹）、叙事结构机制。
- **不搬**：原片文案字幕、标题、分镜顺序、人设序列、作者名/水印/logo、人物肖像、版权角色（学构造手法，画明显不同的原创角色）、原片配乐。
- 复刻是学机制，不是逐像素。用户说「一比一复刻」时照做，并一句话说明「风格一比一，内容不搬」。
- 示例文案自己写，换一个与原片不同的题目。

## 0. 拿到原片 + 定 ID
- 抖音：`python3 $SD/scripts/fetch_douyin.py "<分享文本>" --out <项目>/蒸馏/<风格ID>/原片.mp4`（同时写标题/作者/数据 json）。YouTube/B站等用 `yt-dlp`；公版画作参考用 `uv run $SD/scripts/fetch_reference.py --out 参考/<名> "<关键词>"`。
- 风格 ID：英文 kebab-case（`pixel-relay`），中文名 3–6 字（像素传话风）。
- 拆解产物放 `<项目>/蒸馏/<风格ID>/`，不进任何公开仓库。

## 1. 机器拆解（两套脚本互补，都跑）
```sh
cd <项目>/蒸馏/<风格ID>
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate -of default=nw=1 原片.mp4
uv run --with numpy --with pillow python $SD/scripts/analyze.py 原片.mp4 --out 报告   # report.md：镜头表、运动强度、主色板+强调色、响度、卡点（beats.py）
uv run $SD/scripts/breakdown.py --video 原片.mp4 --out 拆解                            # 逐帧差、转场起点+节拍网格拟合、转场接触表、运动热图、关键帧总览
```
- 先读 `报告/report.md` 和 `拆解/cuts.json`。切点太多/太少调 `analyze.py --cut`（默认 0.30）或 `breakdown.py --thresh/--debounce`。
- 转场起点间隔若是常数整数倍 → 有 BPM 网格，之后所有时间写成「第几拍」。
- 运动热图必看：没有这一步，做出来就是「图片之间的转场」，丢掉镜内连续运动。
- 长片渲染/拆解用 background shell（单条命令 120 秒上限）。

## 2. 人眼拆解（读 `references/weilanx-拆解方法.md` + `references/huashu-01-拆解.md`）
1. **结构**：硬切少镜头长 → 学元素进出；硬切多 → 学切点和构图；运动强度低+尖峰 → 尖峰就是招牌时刻。
2. **画面分类**：联系表分出几类画面（标题卡、固定版式、图表、实物、UI……），每类 2–3 个代表帧 = 素材包里的一组组件。
3. **固定版式**：哪些元素总在同一位置（角标、字幕、卡片）。
4. **细节**：`ffmpeg -ss T -i 原片 -frames:v 1 -vf crop=…` 放大看字体/描边/阴影/质感；PIL `getpixel` 取色（四角+中心判断光晕暗角）。
5. **动效切片**：`uv run --with pillow python $SD/scripts/strip.py 原片.mp4 --at 16.6 --span 1.2 --n 8 --out strips/t16.6.jpg`。数几帧完成、缓动类型（ease-out / in-out / 回弹）、有无模糊缩放位移。转场取「转场开始前最后一帧」作参考帧。
6. **叙事机制**：这片为什么好看、为什么被转发——钩子、结构、反转、结尾。速通/穿越类读 `references/huashu-02-速通类机制.md` 的五层机制。
7. **音频**：读 `references/huashu-05-节奏与配乐.md`。画面节点是否卡小节线、高潮是否踩换气+重拍。模型「听」出的 BPM 只当候选，用起音检测回校。
8. **多支视频**：各自拆完列对照表，一致的进「特征」，不一致的做成参数或「变体」。跨作品提炼（艺术家/工作室风格）读 `references/huashu-15-跨场景风格提炼.md`：至少 3 个独立样本，区分于最近邻风格的两点。

## 3. 写风格配方卡（设计稿，写清再动手）
按 `references/配方卡模板.md`：一句话定位、底色质感、配色（带色值）、字体、固定版式、出场（帧数+缓动）、转场、镜头、节奏（平均镜头长、BPM）、招牌画面、叙事机制、组件清单、「没有搬的东西」、状态。每条尽量带数字。放 `<项目>/蒸馏/<风格ID>/配方卡.md`。

## 4. 落地成代码（二选一）
- **Remotion（weilanx 工程）**：照 weilanx distill skill 第 4–7 步，在 `/workspace/skills/weilanx-claude-videos` 写 `src/library/<风格ID>/`（theme.ts / stage.tsx / props.tsx / charts.tsx）、`src/library/previews/<Name>Demo.tsx`、注册 `library-<风格ID>`、配方卡进 `styles/我的风格/<中文名>/`。硬规则：动画是帧号纯函数、随机用 `rand(seed)`、字体须可再分发。命令前 `export NODE_OPTIONS=--max-old-space-size=4096`；`npx remotion still … --frame=N` 一次只渲一帧。
- **Playwright 引擎（huashu 工程）**：`cp -R /workspace/skills/huashu-art-motion/scripts/engine <项目>/代码工程`，写 `scenes/<id>.js`，`render.py --solo <id> --stills …` 出静帧。适合艺术画风类。

## 5. 对照自查（至少两轮）
- 同类画面左右拼：`ffmpeg -i 原片帧 -i 我们的帧 -filter_complex hstack 对比.jpg`；画作类用 `uv run $SD/scripts/side_by_side.py --ref 参考/<名> --frame <我们的帧> --out 对照.jpg`。
- 逐项对：底色、主色、强调色、字体气质、字号层级、版式位置、质感、留白；动效切片对帧数和缓动。
- 静帧好看不证明动画流畅，动态单独核。
- 去掉名字和标志物后仍认得出风格吗？和近邻风格并排有实际差别吗？

## 6. 交付
- 给用户：风格要点 3–5 条、组件清单、自查改了什么、有意没搬什么、还没做到的。预览用 display_file 发静帧拼图或一段预览 mp4（用户看不到 localhost Studio），不发路径。
- 状态诚实：只拆了没实现 = 研究配方；做了一个场景 = 单场景实做；换不同题材通过对照 = 跨场景验证。
- 用户要马上用它出片时，接着用对应出片工作流（weilanx-claude-videos 的子 skill 或 huashu-art-motion）。
