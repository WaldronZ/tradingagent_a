import getpass
import requests
from rich.console import Console
from rich.panel import Panel

from cli.config import CLI_CONFIG


def fetch_announcements(url: str = None, timeout: float = None) -> dict:
    """
    从接口获取公告，返回包含公告内容与配置的字典。
    
    参数：
        url: 请求地址。
        timeout: 超时时间。
    
    返回：
        dict: 外部查询返回的数据。
    """
    endpoint = url or CLI_CONFIG["announcements_url"]
    timeout = timeout or CLI_CONFIG["announcements_timeout"]
    fallback = CLI_CONFIG["announcements_fallback"]

    try:
        response = requests.get(endpoint, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return {
            "announcements": data.get("announcements", [fallback]),
            "require_attention": data.get("require_attention", False),
        }
    except Exception:
        return {
            "announcements": [fallback],
            "require_attention": False,
        }


def display_announcements(console: Console, data: dict) -> None:
    """
    展示公告面板；当 require_attention 为 True 时提示按回车继续。
    
    参数：
        console: 用于输出的控制台对象。
        data: 输入数据。
    
    返回：
        None: 无返回值。
    """
    announcements = data.get("announcements", [])
    require_attention = data.get("require_attention", False)

    if not announcements:
        return

    content = "\n".join(announcements)

    panel = Panel(
        content,
        border_style="cyan",
        padding=(1, 2),
        title="Announcements",
    )
    console.print(panel)

    if require_attention:
        getpass.getpass("Press Enter to continue...")
    else:
        console.print()
