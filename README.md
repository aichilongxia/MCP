# MCP Python SDK demo (FastMCP)

这是一个最小可运行的 MCP Server + MCP Client demo，基于官方 `python-sdk` 的 FastMCP quickstart。

## 环境

- Windows + PowerShell
- 已安装 `uv`（并且 `uv` 在 `PATH` 里）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"


如果你的 `uv` 在 `C:\Users\admin\.local\bin`，可以在当前终端执行：

```powershell
$env:Path = "C:\Users\admin\.local\bin;$env:Path"
```

## 运行 demo 

在本仓库根目录运行：

```powershell
uv run python mcp_client.py
```

它会自动用 stdio 启动本地的 `mcp_server.py` 子进程 （一般来说是client是连接sever的，但是run server.py无法把信息从studio传出去，因此最好用uv run python mcp_client.py），然后：

- 列出 prompts/resources/tools
- 获取 `greet_user` prompt 的渲染结果
- 读取 `greeting://World` resource
- 调用 `add` 和 `server_info` tool

你也可以单独运行 server（stdio）： 
也可以开启Http流水线，监听一个端口：用于测试api调用是否正常

```powershell
uv run python mcp_server.py
```

## 用 MCP Inspector 调试（可选）

```powershell
uv run mcp dev mcp_server.py 会开启一个界面记录和展示 MCP Server 的交互日志，方便调试和查看 Agent 调用工具的过程。
```

或者直接在 VSCode 中加入到 launch.json 的 debug 配置里，设置好环境变量和工作目录，就可以直接在 VSCode 中调试 MCP Server 了，非常方便。

```json
{
    "name": "Debug MCP Server",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/mcp_server.py",
    "env": {
        "PATH": "C:\\Users\\admin\\.local\\bin;${env:PATH}"
    },
    "console": "integratedTerminal"
}
```

> 依赖已使用 `mcp[cli]` 安装。

**远程开发**
部署到https://horizon.prefect.io/huan-mcp-v1/servers/inland-scarlet-wolverine/clients 连接的GitHub repo里，直接push就可以了，非常方便。 只是连接一次就可以，每次push自动更新

踩坑：build会起一个container，它默认会装fastmcp 包会指定版本，导致本地安装的fastmcp版本和container里不一致，可能会出现一些问题。解决办法是把本地的fastmcp版本也指定为2.12.3，这样就不会有版本不一致的问题了。因此一定要看打包的版本，保持本地和远程一致， 写在requirements.txt里。


MCP总结：
MCP建立在function calling上面， agent自动识别要用到哪些mcp的资源，并且自动调用 （一般而言reAct模式会循环调用tools）（在function calling基础上用了一层json-rpc协议转换，本质还是用name + description选择tool, 代码负责流程）适合与外部系统沟通访问

- MCP 是一个协议规范，定义了 Agent、Tool、Prompt、Resource 等概念，以及它们之间的交互方式。
- FastMCP 是 MCP 的 Python SDK 实现，提供了一个简单的接口来创建 MCP Server 和 Client。
- 通过 FastMCP，我们可以快速搭建一个 MCP Server，定义一些 prompts、resources 和 tools，然后通过 MCP Client 来调用它们，实现 Agent 的功能。

**MCP和SKills的区别**
- **MCP** 提供了一些tools resource, prompt的概念, 它可以本地运行, 也可以远程调用. 这和SKills的概念很像, 但是MCP更底层一些, 更灵活一些. MCP能够让定义server 和client的交互, 也就是说, 你可以在本地定义一个MCP server, 然后在远程调用它的tools和prompts. 这对于构建分布式的Agent系统非常有用. MCP还支持多种通信方式, 包括stdio, websocket等, 这使得它可以适应不同的应用场景. 比如订票这种专业极强的场景, 外部的系统可能已经提供了一个API, 你可以通过MCP来封装这个API, 让Agent能够调用它, 而不需要关心底层的实现细节. 总的来说,MCP是一个非常有用的工具, 可以帮助我们构建更加强大和灵活的Agent系统.

- **Skill** 它也是在function callingd的基础上, 但是它更高层一些, 它提供了一个框架来定义技能, 包括技能的输入输出, 以及技能的执行逻辑. Skill更关注于技能的定义和管理（name + description + script）, 偏向于运行于本地terminal端（直接命令行调用 + 文字化定义流程），构建一个技能库, 让Agent能够调用这些技能来完成任务. Skill也支持多种技能类型, 包括工具型技能, 对话型技能等, 这使得它可以适应不同的应用场景. 比如在客服场景中, 你可以定义一个查询订单状态的技能, 让Agent能够调用这个技能来帮助用户查询订单状态. 总的来说, Skill是一个非常有用的工具, 可以帮助我们构建更加强大和灵活的Agent系统. 适合与本地规范化流程（代码审查）

它提供了很多tools，
 - 本地可以用mcp client load进来，
tools = await client.list_tools()  
 - 也可以给LLM调用，LLM的create_message里可以指定tools参数，LLM就能调用这些tools了。返回的结果中也可以包含要调用的tool，client就会自动调用这个tool并把结果返回给LLM。这样就实现了Agent调用工具的功能，非常方便。
from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "inland-scarlet-wolverine",
            "server_url": "https://inland-scarlet-wolverine.fastmcp.app/mcp",
            "require_approval": "never",
        },
    ],
    input="Hello from Horizon!",
)

 - or 直接在 VSCode中加入到 launch.json 的 debug 配置里，设置好环境变量和工作目录，就可以直接在 VSCode 中调试 MCP Server 了，非常方便。
code --% --add-mcp "{\"name\":\"inland-scarlet-wolverine\",\"type\":\"http\",\"url\":\"https://inland-scarlet-wolverine.fastmcp.app/mcp\"}"


**Links**
 - https://cloud.tencent.com/developer/article/2631910
 - https://developer.volcengine.com/articles/7535837693893148723
 - https://github.com/modelcontextprotocol/python-sdk (它用的是mcp.server.fastMCP，和单独的fastmcp包不太一样)
 - https://www.youtube.com/watch?v=EPXcIFFSv8k