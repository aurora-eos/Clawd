# Version 2 quality checks / 新版检查记录

Date / 日期：2026-11-05

## Art direction / 造型

Redrawn in response to the supplied reference: a flat muted-orange rectangular body, four thin feet, minimal eyes, no shell outline or glossy shading. All 24 expressions share the same character rig. Expanded to 15 everyday scenes and 9 moods. The supplied chat screenshot is a visual reference and is not redistributed in the repository.

根据用户提供的参考图重绘：扁平橘色方块、四只细短脚、简洁眼睛，移除厚描边及外壳高光。24 款共用角色造型，包含 15 个生活场景和 9 个情绪动作。用户聊天截图仅作为视觉参考，不打包发布。

## Assets / 素材

- All 24 GIFs decode successfully, with transparent backgrounds and infinite loops. 128 × 128 native pixels, 48 timeline samples at 80 ms each, 3,840 ms total. Identical neighboring frames may merge during GIF encoding; held poses are intentional.
- All 24 PNGs are 512 × 512 RGBA, with both transparent and opaque pixels.
- Every decoded GIF frame has nonempty artwork entirely inside the canvas boundary.
- Inspected the full contact sheet for consistent shape, unclipped props and scene readability. Exported a four-scene animated overview in `preview/scene-loops.gif`.
- 24 个 GIF 全部逐帧解码通过，透明、无限循环、时长一致，无边界裁切；24 张 PNG 全部透明。已检查全套总览及场景构图，并导出四场景动态预览。

## Browser / 浏览器

Local Chromium checks passed at 320 × 740, 390 × 844, 768 × 1024, 1024 × 768 and 1440 × 1000:

- 24 cards and 48 download links; every preview decoded after scrolling into view.
- No horizontal overflow or JavaScript errors.
- Scene filter shows 15 cards; mood filter shows 9; reset shows all 24.
- Pause/play switches PNG/GIF; transparency checker toggle works; reduced-motion starts paused.
- All 48 resource URLs returned HTTP 200; actual browser download succeeded as `clawd-typing.gif`.

手机、平板及桌面 5 种视口通过；筛选、暂停播放、透明棋盘、减少动态效果及实际下载通过。测试使用 Chromium 视口模拟，未进行实体 iPhone/iPad 或 Safari 测试。

## Per-file decoding / 逐文件解码

| Sticker | Encoded frames | Duration ms | GIF bytes |
|---|---:|---:|---:|
| wave | 13 | 3840 | 13679 |
| yay | 41 | 3840 | 45010 |
| love | 25 | 3840 | 27358 |
| typing | 47 | 3840 | 67005 |
| think | 7 | 3840 | 8011 |
| sleep | 25 | 3840 | 32054 |
| cry | 19 | 3840 | 21294 |
| angry | 25 | 3840 | 27413 |
| wow | 14 | 3840 | 15209 |
| coffee | 7 | 3840 | 8765 |
| dance | 33 | 3840 | 39235 |
| hug | 13 | 3840 | 13840 |
| bubbles | 48 | 3840 | 58834 |
| rain | 48 | 3840 | 61692 |
| gift | 13 | 3840 | 15404 |
| garden | 19 | 3840 | 24918 |
| noodles | 13 | 3840 | 16553 |
| kite | 17 | 3840 | 22327 |
| read | 22 | 3840 | 29895 |
| toast | 12 | 3840 | 15647 |
| camp | 15 | 3840 | 23121 |
| paint | 13 | 3840 | 17762 |
| scooter | 22 | 3840 | 25844 |
| bath | 46 | 3840 | 59845 |

Reproduce / 重现：`python scripts/check_assets.py`

Remote version 2 deployment / 新版线上部署：verification pending / 待验证。
