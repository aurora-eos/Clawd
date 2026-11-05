# Quality checks / 质量检查

Checked locally on 2026-11-05 / 本地检查日期：2026-11-05。

- All 12 GIFs decoded frame by frame: transparent backgrounds, infinite loop, 1,920 ms duration, nonempty animation and no artwork touching canvas boundaries. All 12 PNGs are 384 × 384 RGBA with transparent backgrounds.
- 已逐帧解码全部 12 个 GIF；透明、无限循环、时长一致、无边界裁切。12 张 PNG 均为 384 × 384 透明图。
- Reviewed the contact sheet and decoded frame strips for all expressions: one shared silhouette, palette and pixel grid. Replaced mismatched particle/steam/tear periods with periodic motion; increased sampling from 16 × 110 ms to 32 × 60 ms. Confetti now stays inside safe canvas bounds. Identical neighboring frames are merged by GIF encoding while retaining their duration.
- 已审阅全部表情总览和逐帧图：造型、色板和像素网格一致；修正粒子、蒸汽、眼泪周期，提升动画采样率，并修复彩纸边界裁切。GIF 编码合并相邻重复帧但保留时长。
- Chromium responsive checks: 320 × 740, 390 × 844, 768 × 1024, 1024 × 768, 1440 × 1000. Every viewport: 12 cards, all preview images decoded, 24 download links, no horizontal overflow, no JavaScript errors. Pause/play and reduced-motion preference passed. All 24 resource URLs returned HTTP 200 locally; an actual browser download produced `clawd-wave.gif`.
- 已通过上述手机、平板和桌面视口检查；暂停、播放及系统减少动态效果正常。
- These are browser viewport simulations; physical iPhone/iPad and Safari were not available for testing. / 这是浏览器视口模拟，未进行实体 iPhone/iPad 或 Safari 测试。

Reproduce asset checks / 重现素材检查：`python scripts/check_assets.py`.

| Sticker | Encoded frames | Duration (ms) | Seam changed pixels | Largest frame step |
|---|---:|---:|---:|---:|
| wave | 26 | 1920 | 2 | 580 |
| yay | 32 | 1920 | 148 | 792 |
| love | 32 | 1920 | 119 | 630 |
| typing | 32 | 1920 | 6 | 789 |
| think | 24 | 1920 | 2 | 525 |
| sleep | 28 | 1920 | 2 | 584 |
| cry | 30 | 1920 | 369 | 838 |
| angry | 31 | 1920 | 343 | 836 |
| wow | 26 | 1920 | 2 | 524 |
| coffee | 31 | 1920 | 18 | 601 |
| dance | 31 | 1920 | 42 | 875 |
| hug | 28 | 1920 | 2 | 544 |

Seam metrics compare the last decoded frame with the first. They support the visual review; they do not measure subjective smoothness. / 接缝像素指标用于辅助视觉检查，不能量化主观流畅度。

Remote repository and Pages verification: pending GitHub CLI authorization. / 远端仓库及 Pages 验证：等待 GitHub CLI 授权。
