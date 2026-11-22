# examples

示例输入，不是真实客户数据。

- `leads_example.csv`：`lead_score.py` 的示例输入，共 10 条线索。表头是脚本认的 9 列：`company,country,product,source,email,phone,years,contact,note`，只有 `company` 必填。换真实数据时，先 `cp examples/leads_example.csv my_leads.csv`，只往 `my_leads.csv` 里填——`my_leads.csv` 会被 `.gitignore` 挡住，不会传上网。
- `leads_example_lighting.csv`：非轮胎行业示例，LED 灯具 8 条线索（T0:0/T1:2/T2:2/T3:4）。同一张表头，证明这套分级不只认轮胎；但注意品类词只认轮胎词（tyre/tire/tube/rim 等），LED 行拿不到那 4 分，所以同样条件 LED 最高只到 T1——这不是 bug，是评分口径本来就是按轮胎调的。
- `trade_show_example.csv`：`trade_show.py` 的示例输入，3 家展会名片（高/中/低兴趣各一）。

公司名统一带「」前缀，邮箱用保留域名 `sample.example`，电话是占位符。请不要照着去联系任何人。
