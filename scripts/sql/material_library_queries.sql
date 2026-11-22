-- ============================================================
-- 素材库文件清单 10 条查询（SQLite）
-- 数据集：~/workspace/museai外贸/素材库/（2026-11-22 实测 919 个文件）
-- 用途：John 的 SQL 入门练手 + 12-04 验数①（10 条查询能跑通）
-- 落盘：2026-11-22（本地未提交、未推送，推送须 John 批）
-- 复核：2026-11-22 重数，10 条结果与 2026-11-21 全部一致，0 变
-- ============================================================
-- 建表（入库方法见文件末尾注释）：
--   path        TEXT    -- 相对路径，如 extracted/pack_27/xxx.jpg
--   name        TEXT    -- 文件名，如 xxx.jpg
--   ext         TEXT    -- 小写扩展名，如 .jpg；无扩展名为空串 ''
--   size_bytes  INTEGER -- 文件大小（字节）
--   parent_dir  TEXT    -- 相对父目录，如 extracted/pack_27；根目录文件记 '(root)'
--   top_dir     TEXT    -- 顶层目录，如 extracted / inbox / bgm
-- ============================================================

CREATE TABLE IF NOT EXISTS files (
    path       TEXT,
    name       TEXT,
    ext        TEXT,
    size_bytes INTEGER,
    parent_dir TEXT,
    top_dir    TEXT
);

-- Q1：文件总数（2026-11-22 复核：919，与 11-21 一致）
SELECT COUNT(*) AS total_files FROM files;

-- Q2：按扩展名分组 TOP 5（2026-11-22 复核：.jpg 458、.png 133、.docx 77、.pdf 66、.zip 48，与 11-21 一致）
SELECT ext, COUNT(*) AS n FROM files GROUP BY ext ORDER BY n DESC;

-- Q3：图片 + 视频文件数（2026-11-22 复核：615，与 11-21 一致）
SELECT COUNT(*) AS image_video_files
FROM files
WHERE ext IN ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp',
              '.mp4', '.mov', '.avi', '.mkv', '.webm');

-- Q4：按父目录分组 TOP 3（2026-11-22 复核：extracted/pack_27 205、pack_26 111、pack_25 85，与 11-21 一致）
SELECT parent_dir, COUNT(*) AS n FROM files GROUP BY parent_dir ORDER BY n DESC;

-- Q5：大于 1MB 的文件数（2026-11-22 复核：199，与 11-21 一致）
SELECT COUNT(*) AS over_1mb FROM files WHERE size_bytes > 1048576;

-- Q6：平均文件大小（2026-11-22 复核：1,720,594.74 字节，四舍五入 1,720,594，与 11-21 一致）
SELECT ROUND(AVG(size_bytes), 2) AS avg_bytes FROM files;

-- Q7：最大文件（2026-11-22 复核：微信图片_20260703094043_301_7362.jpg，33,291,502 字节，与 11-21 一致）
SELECT name, size_bytes FROM files ORDER BY size_bytes DESC LIMIT 1;

-- Q8：目录数（按全部层级的相对父目录去重；2026-11-22 复核：36，与 11-21 一致）
SELECT COUNT(DISTINCT parent_dir) AS dir_count FROM files;

-- Q9：无扩展名文件数（2026-11-22 复核：0，与 11-21 一致）
SELECT COUNT(*) AS no_extension FROM files WHERE ext = '';

-- Q10a：文件名含 2026 的文件数（2026-11-22 复核：411，与 11-21 一致）
SELECT COUNT(*) AS filename_contains_2026 FROM files WHERE name LIKE '%2026%';

-- Q10b：全路径含 2026 的文件数（2026-11-22 复核：468，与 11-21 一致；
--   与 Q10a 差 57 个，来自目录名 inbox/2026-09-29_63文件_留学资料包；
--   Q10 标准口径为文件名 411 个）
SELECT COUNT(*) AS fullpath_contains_2026 FROM files WHERE path LIKE '%2026%';

-- ============================================================
-- 入库方法（任选其一；本文件只含建表 + 查询，不含数据行）：
--   A. Python 入库（已实测 2026-11-21、2026-11-22 两轮）：
--      os.walk 遍历素材库 → 每文件一行 (path, name, ext, size_bytes,
--      parent_dir, top_dir) → sqlite3 executemany 写入 files 表。
--   B. sqlite3 CLI：.mode csv + .import 清单.csv files（须先导出文件清单 CSV）。
-- 复跑：sqlite3 素材库.db < 本文件（须先建库入库；查询本身不写库）。
-- 注意：SQLite CSV 虚拟表（csv.html）不是内置功能，须另编译扩展
--   并 .load 才能用；对入门者更顺的路仍是先入库再查（方法 A/B）。
-- ============================================================
