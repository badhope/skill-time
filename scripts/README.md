# Scripts

此目录包含项目相关的脚本工具。

## release.py

版本发布脚本，用于自动化版本发布流程。

### 使用方法

```bash
# 指定版本号发布
python scripts/release.py --version 0.1.0

# 自动升级版本号
python scripts/release.py --bump patch  # 0.1.0 -> 0.1.1
python scripts/release.py --bump minor  # 0.1.0 -> 0.2.0
python scripts/release.py --bump major  # 0.1.0 -> 1.0.0

# 跳过某些步骤
python scripts/release.py --version 0.1.0 --skip-tests
python scripts/release.py --version 0.1.0 --skip-build
python scripts/release.py --version 0.1.0 --skip-tag
```

### 功能

- 自动更新 `__init__.py` 和 `setup.py` 中的版本号
- 运行单元测试
- 构建包（生成 `dist/` 目录）
- 创建 Git 标签

### 发布流程

1. 确保所有更改已提交
2. 运行 `python scripts/release.py --bump patch`
3. 检查 `dist/` 目录下的构建文件
4. 运行 `git push && git push --tags` 推送更改和标签
