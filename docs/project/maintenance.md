# 维护规则

## 纯文档约束

仓库允许：

- Markdown 文档。
- `LICENSE`、`.gitignore` 等必要的仓库元文件。

仓库不允许：

- 比赛、模拟和个人工作记录。
- 数据、代码、Notebook 和可执行脚本。
- 图片、PDF、Word、Excel、压缩包和论文模板。
- 完整复制的第三方 Skill 或 README。

## 上游同步

检查三个上游项目时，只回答：

1. 定位是否改变？
2. 推荐用户是否改变？
3. 关键门禁或交付格式是否改变？
4. 链接和安装入口是否仍有效？

如果只是内部实现、文件数量或脚本参数变化，优先保持 Hub 文档抽象稳定并链接到上游。

## 文档审查

每次修改至少检查：

```bash
# 仓库中是否出现非文档业务文件
find . -type f -not -path './.git/*' \
  -not -name '*.md' -not -name LICENSE -not -name .gitignore

# 是否残留比赛运行时路径
rg -n 'competitions/|Simulation/|Person1|Person2|Coder/' --glob '*.md'
```

还应检查所有相对 Markdown 链接确实存在。外部链接可能受网络限制，至少确认 URL 使用 HTTPS 且指向明确项目页面。

## 内容决策

新增内容同时满足以下条件才进入 Hub：

- 对多个比赛或多个团队可复用。
- 不依赖某一届题目的具体数据。
- 能明确说明适用条件和失败边界。
- 不与上游实现形成需要双份同步的副本。
