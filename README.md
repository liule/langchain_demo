# Kimi + LangChain 天气搜索 Agent

这个示例实现了一个基于 **LangChain** 的 Agent，接入 **Kimi（Moonshot）大模型服务**，并支持：

- 搜索（DuckDuckGo）
- 查询当前天气（wttr.in）

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 配置环境变量

复制示例配置：

```bash
cp .env.example .env
```

编辑 `.env`，至少填入：

- `MOONSHOT_API_KEY`

可选：

- `MOONSHOT_BASE_URL`（默认 `https://api.moonshot.cn/v1`）
- `KIMI_MODEL`（默认 `moonshot-v1-8k`）
- `TAVILY_API_KEY`（本示例默认用 DuckDuckGo，不强制）

## 3. 运行

```bash
python weather_search_agent.py
```

示例问题：

- `北京现在天气怎么样？`
- `帮我搜索今天上海的天气新闻，并告诉我适合穿什么。`

## 4. 说明

- 天气数据来自 `wttr.in` 免费接口。
- 搜索工具使用 `DuckDuckGoSearchRun`，无需额外 API Key。
- 如果你希望更稳定的搜索结果，可以替换成 Tavily 工具。
