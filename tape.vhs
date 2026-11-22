# zero-to-trade 终端演示录制脚本（VHS v0.10.0）
# 用法：在仓库根目录跑 ~/.local/bin/vhs tape.vhs（需先装 VHS：https://github.com/charmbracelet/vhs/releases）
# 产出 assets/demo.gif（<5MB），README 首屏引用。示例数据全是虚构的，不含真实客户信息。
Output assets/demo.gif
Set FontSize 15
Set Width 1180
Set Height 760
Set Shell "bash"
Hide
Type "python3 scripts/lead_score.py examples/leads_example.csv"
Enter
Sleep 3s
Show
Sleep 2s
