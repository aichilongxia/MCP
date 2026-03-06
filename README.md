# MCP Python SDK demo (FastMCP)

这是一个最小可运行的 MCP Server + MCP Client demo，基于官方 `python-sdk` 的 FastMCP quickstart。

## 环境

- Windows + PowerShell
- 已安装 `uv`（并且 `uv` 在 `PATH` 里）

如果你的 `uv` 在 `C:\Users\admin\.local\bin`，可以在当前终端执行：

```powershell
$env:Path = "C:\Users\admin\.local\bin;$env:Path"
```

## 运行 demo

在本仓库根目录运行：

```powershell
uv run python mcp_client.py
```

它会自动用 stdio 启动本地的 `mcp_server.py` 子进程，然后：

- 列出 prompts/resources/tools
- 获取 `greet_user` prompt 的渲染结果
- 读取 `greeting://World` resource
- 调用 `add` 和 `server_info` tool

你也可以单独运行 server（stdio）：

```powershell
uv run python mcp_server.py
```

## 用 MCP Inspector 调试（可选）

```powershell
uv run mcp dev mcp_server.py
```

> 依赖已使用 `mcp[cli]` 安装。
