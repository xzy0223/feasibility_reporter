# Feasibility Reporter

基于 CrewAI 的可行性分析报告生成器，能够自动分析需求、技术可行性，并生成详细的报告。

## 功能特点

- 需求分析：自动分析和理解项目需求
- 技术分析：评估技术可行性和最佳实践
- 自动报告生成：生成结构化的可行性分析报告
- AWS Bedrock 集成：使用高级AI模型进行分析
- GitHub 集成：支持代码库分析和最佳实践研究

## 安装要求

- Python 3.10-3.12
- AWS 账户（用于 Bedrock 服务）
- GitHub Token（用于代码库分析）

## 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/xzy0223/feasibility_reporter.git
cd feasibility_reporter
```

2. 创建并激活虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -e .
```

4. 配置环境变量：
```bash
cp .env.example .env
```
编辑 .env 文件，填入必要的环境变量：
```
MODEL=bedrock/your-model-name
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION_NAME=your_aws_region
GITHUB_TOKEN=your_github_token
```

## 使用方法

运行可行性分析：
```bash
crewai run
```

## 项目结构

```
feasibility_reporter/
├── src/
│   └── feasibility_reporter/
│       ├── config/           # 配置文件
│       │   ├── agents.yaml   # AI代理配置
│       │   └── tasks.yaml    # 任务配置
│       ├── tools/            # 自定义工具
│       ├── crew.py          # CrewAI实现
│       └── main.py          # 主程序入口
├── .env.example             # 环境变量示例
└── pyproject.toml           # 项目配置
```

## 工作流程

1. Requirement Analyst（需求分析专家）分析项目需求
2. Tech Analyst（技术分析专家）评估技术可行性
3. Reporting Analyst（报告专家）生成最终报告

分析结果将保存在 `report.md` 文件中。

## 注意事项

- 确保所有敏感信息（API密钥、访问令牌等）都存储在 .env 文件中
- .env 文件已被添加到 .gitignore，不会被提交到版本控制系统
- 使用前请确保已正确配置所有必要的环境变量

## License

MIT License
