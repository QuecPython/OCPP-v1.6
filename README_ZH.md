# OCPP

中文 | [English](./README.md)

## 介绍

该项目基于 QuecPython 进行开发使用。

Python 包实现了开放充电点协议（OCPP）的 JSON 版本。目前支持 OCPP 1.6（勘误表 v4）。

该库的目的是提供构建充电站/充电点的构建块。 **该库不提供完整的解决方案，因为任何实现都是特定于其预期用途的**。应检查该库中的文档，因为这些文档提供了有关如何最好地构建完整解决方案的指导。

## 快速开始

您可以在下面找到有关如何创建简单的 OCPP 1.6 充电站/充电点的示例。

**注意：**

> 要运行这些示例，需要依赖项 uwebsocket ！该文件位于 `code/tools/uwensocket.py` 中。

## 充电站 / 充电点

`v16_client_qpy_demo.py` 是充电站 / 充电点样例代码。

```python
import modem
import utime
import _thread

from usr.tools import uwebsocket, logging
from usr.ocpp.routing import on
from usr.ocpp.v16 import ChargePoint as cp
from usr.ocpp.v16.enums import RegistrationStatus, Action

logger = logging.getLogger(__name__)

IMEI = modem.getDevImei()


class ChargePoint(cp):

    def send_boot_notification(self):
        request = self._call.BootNotificationPayload(
            charge_point_model="ICU Eve Mini",
            charge_point_vendor="Alfen BV",
            firmware_version="#1:3.4.0-2990#N:217H;1.0-223"
        )
        response = self.call(request)
        logger.info("response %s" % response)

        if response.status == RegistrationStatus.accepted:
            logger.info("Connected to central system.")

    @on(Action.CancelReservation)
    def on_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))

        return self._call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )


if __name__ == "__main__":
    # Init websocket client.
    ws = uwebsocket.Client.connect(
        "ws://xxx.xxx.xxx.xxx:xxxx/%s" % IMEI,
        headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
        debug=True
    )

    # Init ChargePoint.
    cp = ChargePoint(IMEI, ws)

    # Start websocket receiving thread.
    _thread.stack_size(0x2000)
    tid = _thread.start_new_thread(cp.start, ())
    utime.sleep_ms(200)

    # Send boot notification.
    cp.send_boot_notification()
```

## 项目文件说明

```shell
|-- code
    |-- ocpp
        |-- v16
            |-- __init__.py
            |-- call_reasult.py
            |-- call.py
            |-- datatypes.py
            |-- enums.py
        |-- charge_point.py
        |-- dataclasses.py
        |-- exceptions.py
        |-- messages.py
        |-- routing.py
    |-- tools
        |-- logging.py
        |-- uuid.py
        |-- uwebsocket.py
    |-- v16_client_qpy_demo.py
|-- demo
    |-- requirements.txt
    |-- v16_server_demo.py
|-- docs
    |-- docs/en
        |-- docs/en/API_Reference.md
    |-- docs/zh
        |-- docs/zh/API说明手册.md
    |-- OCPP_1.6_documentation_2019_12-2.zip
```

- `code` 目录包含所有 OCPP 客户端代码。
  - `code/ocpp` 目录包含了所有 OCPP 客户端协议代码
    - `code/ocpp/v16/call.py` 包含所有请求数据的格式
    - `code/ocpp/v16/call_result.py` 包含所有应答数据的格式
    - `code/ocpp/v16/datatypes.py` 包含部分请求数据的某种数据结构
    - `code/ocpp/v16/enums.py` 包含部分请求/响应数据的枚举值
    - `code/ocpp/charge_point.py` 为充电点抽象类
  - `code/tools` 目录包含一些辅助功能模块
    - `code/tools/logging.py` 日志模块
    - `code/tools/uuid.py` UUID 生成模块
    - `code/tools/uwebsocket.py` Websocket 客户端模块
  - `code/ocpp/v16_client_qpy_demo.py` 包含了充电点/充电站所有请求和接收数据示例
- `demo` 目录包含基于 CPython 的 OCPP 协议的服务端示例代码
  - `demo/requirements.txt` OCPP 服务器示例代码运行环境依赖包
  - `demo/v16_server_demo.py` 基于 CPython 的 OCPP 服务器示例代码
- `docs` 目录包含 OCPP 协议文档和 API
  - `docs/OCPP_1.6_documentation_2019_12-2.zip` OCPP v1.6 协议文档

## 如何使用

### 运行 OCPP 服务器

> 如果您有自己的 OCPP 服务器，则可以跳过此说明。

#### 1. 安装环境

- 操作系统：Window or Linux.

- 语言：Python (Python-3.11.2).

- 依赖包：`pip install -r demo/requirements.txt`.

#### 2. 配置服务器并运行演示

- 在 `demo/v16_server_demo.py` 中更改服务器端口。

```python
async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        31499,  # Change this port value for your own server port.
        subprotocols=['ocpp1.6.0']
    )
    logging.info("WebSocket Server Started")
    await server.wait_closed()
```

- 运行 `python demo/v16_server_demo.py`。当输出 `INFO:root:WebSocket Server Started`，则服务端已启动。

```python
>>> python v16_server_demo.py

INFO:websockets.server:server listening on 0.0.0.0:31499
INFO:root:WebSocket Server Started
```

### 运行 OCPP 客户端

#### 1. 运行环境

您需要使用我们的 QuecPython 模块。

#### 2. 配置客户端并运行示例

- 在 `code/ocpp/v16_client_qpy_demo.py` 中配置您的服务器主机和端口

```python
if __name__ == "__main__":
    ws = uwebsocket.Client.connect(
        "ws://xxx.xxx.xxx.xxx:xxxx/%s" % IMEI,  #  Use your own server host and port to replace `xxx.xxx.xxx.xxx:xxxx`.
        headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
        debug=True
    )
    cp = ChargePoint(IMEI, ws)

    _thread.stack_size(0x2000)
    tid = _thread.start_new_thread(cp.start, ())
    utime.sleep_ms(200)
```

- 将代码下载到 QuecPython 模块

**注意：**

> 您可以在 [QuecPython文档中心](https://python.quectel.com/doc/Getting_started/en/index.html) 找到文档，了解如何下载 Python 代码并在我们的 QuecPython 模块中运行 Python 示例

您可以将完整的 `code` 路径下的代码下载到我们的 QuecPython 模块并运行 `v16_client_qpy_demo.py` 来测试 OCPP 充电站/充电点。

您可以在我们的 QPYcom REPL 中看到日志 `Connected to central system.`，则 `BootNotification` 消息已发送到服务器。

**注意：**

> 您可以参考 `code.ocpp.v16_client_qpy_demo.py` 编写符合业务逻辑的客户端请求。

## 用法

- [API 参考手册](./docs/en/API_Reference.md)
- [客户端示例代码](./code/v16_client_qpy_demo.py)
- [服务端示例代码](./demo/v16_server_demo.py)

## 贡献

我们欢迎对本项目的改进做出贡献！请按照以下步骤进行贡献：

1. Fork 此仓库。
2. 创建一个新分支（`git checkout -b feature/your-feature`）。
3. 提交您的更改（`git commit -m 'Add your feature'`）。
4. 推送到分支（`git push origin feature/your-feature`）。
5. 打开一个 Pull Request。

## 许可证

本项目使用 Apache 许可证。详细信息请参阅 [LICENSE](./LICENSE) 文件。

## 支持

如果您有任何问题或需要支持，请参阅 [QuecPython 文档](https://python.quectel.com/doc) 或在本仓库中打开一个 issue。
