#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CI/CD 配置检查脚本
"""

import os
import yaml

print('=' * 60)
print('CI/CD 配置检查')
print('=' * 60)

cicd_path = r'c:\Users\X1882\Desktop\github\skill-time\.github\workflows\ci-cd.yml'

print('\n【检查1】CI/CD 文件存在...')
if os.path.exists(cicd_path):
    print('✓ ci-cd.yml 存在')
else:
    print('✗ ci-cd.yml 不存在')
    exit(1)

print('\n【检查2】解析 CI/CD 配置...')
with open(cicd_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

workflow_name = config.get('name', '未指定')
print(f'✓ 工作流名称: {workflow_name}')

print('\n【检查3】触发条件...')
triggers = config.get('on', {})
if 'push' in triggers:
    print(f'✓ Push 触发: {triggers["push"].get("branches")}')
if 'pull_request' in triggers:
    print(f'✓ PR 触发: {triggers["pull_request"].get("branches")}')
if 'release' in triggers:
    print(f'✓ Release 触发: {triggers["release"].get("types")}')

print('\n【检查4】Jobs 配置...')
jobs = config.get('jobs', {})
for job_name, job_config in jobs.items():
    runs_on = job_config.get('runs-on', '未指定')
    needs = job_config.get('needs', [])
    print(f'  ✓ {job_name}: runs-on={runs_on}, needs={needs}')

print('\n【检查5】依赖关系...')
build_job = jobs.get('build', {})
deploy_job = jobs.get('deploy-pypi', {})
if 'needs' in build_job:
    print(f'✓ Build 依赖于: {build_job["needs"]}')
if 'needs' in deploy_job:
    print(f'✓ Deploy 依赖于: {deploy_job["needs"]}')

print('\n【检查6】安全配置...')
security_job = jobs.get('security', {})
if security_job:
    steps = security_job.get('steps', [])
    for step in steps:
        step_name = step.get('name', '未知')
        if 'bandit' in str(step).lower() or 'safety' in str(step).lower():
            print(f'  ✓ 安全检查: {step_name}')

print('\n【检查7】Python 版本矩阵...')
test_job = jobs.get('test', {})
strategy = test_job.get('strategy', {})
matrix = strategy.get('matrix', {})
python_versions = matrix.get('python-version', [])
print(f'✓ 测试 Python 版本: {python_versions}')

print('\n【检查8】关键配置验证...')

issues = []

# 检查测试覆盖的 Python 版本
if not python_versions:
    issues.append('缺少 Python 版本测试矩阵')
elif len(python_versions) < 3:
    issues.append(f'Python 版本测试不足 (当前{len(python_versions)}个)')

# 检查依赖关系是否正确
if build_job and 'needs' not in build_job:
    issues.append('Build job 缺少依赖声明')

if deploy_job:
    if 'needs' not in deploy_job:
        issues.append('Deploy job 缺少依赖声明')
    elif 'build' not in deploy_job['needs']:
        issues.append('Deploy 应该依赖 Build')

# 检查部署条件
if deploy_job:
    if_condition = deploy_job.get('if', '')
    if 'release' not in if_condition.lower():
        issues.append('Deploy 缺少 release 触发条件')

if issues:
    print('\n⚠️ 发现以下问题:')
    for issue in issues:
        print(f'  - {issue}')
else:
    print('✓ 所有关键配置正确')

print('\n' + '=' * 60)
print('✅ CI/CD 配置检查完成')
print('=' * 60)

print('\n📋 CI/CD 流程总结:')
print('  1. test     - 单元测试 (Python 3.8-3.12)')
print('  2. lint     - 代码风格检查 (Black, isort, Flake8, MyPy)')
print('  3. build    - 构建包')
print('  4. deploy   - 发布到 PyPI (仅在 Release 时)')
print('  5. docs     - 构建文档')
print('  6. security - 安全扫描 (Bandit, Safety)')
