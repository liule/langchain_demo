import os
import requests
from dotenv import load_dotenv

from langchain.agents import AgentType, initialize_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langchain_openai import ChatOpenAI


load_dotenv()


@tool("get_current_weather")
def get_current_weather(location: str) -> str:
    """Get current weather for a location, e.g. 'Beijing' or 'Shanghai'."""
    url = f"https://wttr.in/{location}"
    params = {"format": "j1"}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        current = data["current_condition"][0]
        area = data.get("nearest_area", [{}])[0]
        area_name = area.get("areaName", [{"value": location}])[0]["value"]

        temp_c = current.get("temp_C", "N/A")
        feels_like_c = current.get("FeelsLikeC", "N/A")
        humidity = current.get("humidity", "N/A")
        weather_desc = current.get("weatherDesc", [{"value": "N/A"}])[0]["value"]
        wind_kmph = current.get("windspeedKmph", "N/A")

        return (
            f"{area_name} 当前天气：{weather_desc}，温度 {temp_c}°C，"
            f"体感 {feels_like_c}°C，湿度 {humidity}%，风速 {wind_kmph} km/h。"
        )
    except Exception as e:
        return f"天气查询失败: {e}"


def build_agent():
    api_key = os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        raise ValueError("请先在环境变量中设置 MOONSHOT_API_KEY")

    model_name = os.getenv("KIMI_MODEL", "moonshot-v1-8k")
    base_url = os.getenv("MOONSHOT_BASE_URL", "https://api.moonshot.cn/v1")

    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=0,
    )

    search_tool = DuckDuckGoSearchRun(name="search")
    tools = [search_tool, get_current_weather]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
    )
    return agent


def main():
    agent = build_agent()
    print("Kimi + LangChain Agent 已启动。输入 'exit' 退出。")

    while True:
        query = input("\n你: ").strip()
        if query.lower() in {"exit", "quit"}:
            print("再见！")
            break

        result = agent.run(query)
        print(f"\nAgent: {result}")


if __name__ == "__main__":
    main()
