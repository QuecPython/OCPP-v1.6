# OCPP API 参考手册

中文 | [English](../en/API_Reference.md)

本模块协议功能基于 websocket，使用 json 格式数据进行数据交互。

本模块设计 `ocpp.charge_point.ChargePoint` 抽象类，用来做为基类，用户需要根据自己项目的实际情况进行二次开发，基于该抽象类封装自己项目需要用到的，对应版本的，发送和接收功能。

目前项目只支持 OCPP v1.6 版本，后续会继续进行扩展支持。

本文主要分为两个模块：

1. `ChargePoint` 基类的相关接口与关联装饰器的介绍与使用说明
2. 基于 `ChargePoint` 基类实现数据发送和接收接口的二次开发示例

## 充电站/充电点抽象类

### `ChargePoint`

- `ocpp.charge_point.ChargePoint` 为一个充电站/充电点抽象类
- 该抽象类封装了基于 websocket 协议的数据发送 [`call`](#cp-call) 接口和用于接收服务器消息并处理的 [`start`](#cp-start) 接口。
- 该抽象类的二次开发，需要配合 [`ocpp.routing.on`](#routing-on) 和 [`ocpp.routing.atfer`](#routing-after) 装饰器封装接收消息处理函数。
- 该抽象类通常在对应版本中进行了继承，如：`ocpp.v16.ChargePoint`，添加了 [`_call`](#cp-_call)，[`_call_result`](#cp-_call_result)，[`_ocpp_version`](#cp-_ocpp_version) 属性值
- 该模块基于 websocket 协议，需使用 [QuecPython uwebscoket](https://python.quectel.com/doc/API_reference/zh/networklib/uwebsocket.html "QuecPython uwebsocket 模块使用说明") 模块

#### 初始化

```python
from usr.tools import uwebsocket
from usr.ocpp.v16 import ChargePoint as cp

# 建议使用设备 IMEI 或设备 MAC 地址做为设备唯一标识
IMEI = "XXXX"
# 对应服务器的 IP 地址
host = "xxx.xxx.xxx.xxx"
# 对应服务器的端口号
port = "xxxx"
# 实例化一个 uwebsocket 对象
ws = uwebsocket.Client.connect(
    "ws://{host}:{port}/{IMEI}",
    # 在 header 中添加对应的 OCPP 版本号用于服务端进行识别，不同的服务端有不同的要求，按实际的情况进行填写
    headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
    debug=False
)

# 实例化 ChargePoint 对象
cp = ChargePoint(IMEI, ws)
```

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|id|str|设备标识|
|connection|obj|uwebsocket 实例对象|
|response_timeout|int|请求应答超时时间，单位：秒，默认：30|

**返回值说明：**

|类型|说明|
|:---|:---|
|obj|ChargePoint 客户端实例对象|

#### <span id="cp-start">`ChargePoint.start`</span>

- 启动一个循环用于接收服务器数据，通常单独启动一个线程运行该方法。

```python
import _thread

# 设置线程栈大小，根据实际使用情况设置
_thread.stack_size(0x4000)
# 启动一个线程用于接收和解析服务器下发的数据
_thread.start_new_thread(cp.start, ())
```

#### <span id="cp-call">`ChargePoint.call`</span>

- 向服务端发送 Call 消息并返回响应的有效负载。
- 该方法通常在二次封装的函数中进行使用。

```python
class ChargePoint(cp):

    # 客户端发送请求认证接口
    def send_authorize(self):
        # 使用 AuthorizePayload 类生成客户端请求认证接口的数据结构体
        request = self._call.AuthorizePayload(
            id_tag="xxx",
        )
        # 调用 call 方法发送消息并等待接收应答
        response = self.call(request)
        logger.info("response %s" % response)

        # 判断应答解析后是否为请求认证接口的应答数据结构体，是则进行应答数据的处理
        if isinstance(response, self._call_result.AuthorizePayload):
            logger.info("id_tag_info %s." % response.id_tag_info)
```

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|payload|obj|`vxx.call.xxx` 请求消息数据结构体对象|
|suppress|bool|当请求返回 CallError 时，是否会抛出异常<br>`True` - 跳过异常直接返回<br>`False` - 抛出异常<br>默认：`True`|
|unique_id|str|消息唯一标识，当不传时，则自动生成一个 uuid4 的值做为唯一标识，默认：None|

**返回值说明：**

|类型|说明|
|:---|:---|
|obj|`vxx.call_result.xxx` 应答消息数据结构体对象|

#### <span id="cp-_call">`ChargePoint._call`</span>

- 当从对应版本模块中导入该类时，则会有该属性，为对应版本的 `call` 模块，如：`ocpp.v16.ChargePoint._call` 等价于 `ocpp.v16.call`。
- 该属性主要用于二次开发时，封装接口时方便使用
- [OCPP v1.6 请求消息数据结构](./请求与应答消息数据结构说明_V16.md#request-message-structure)

#### <span id="cp-_call_result">`ChargePoint._call_result`</span>

- 当从对应版本模块中导入该类时，则会有该属性，为对应版本的 `call_result` 模块，如：`ocpp.v16.ChargePoint._call_result` 等价于 `ocpp.v16.call_result`。
- 该属性主要用于二次开发时，封装接口时方便使用
- [OCPP v1.6 应答消息数据结构](./请求与应答消息数据结构说明_V16.md#response-message-structure)

#### <span id="cp-_ocpp_version">`ChargePoint._ocpp_version`</span>

- 当从对应版本模块中导入该类时，则会有该属性，为对应的 ocpp 协议版本号。

## 处理服务器消息的函数的装饰器

### <span id="routing-on">`ocpp.routing.on`</span>

- 该装饰器用于处理对应服务器下发消息的封装函数。
- 被装饰的函数入参为接收消息的数据结构信息，返回对应消息的应答的数据结构信息，用于发送给服务器进行消息应答

```python
class ChargePoint(cp):

    # 客户端接收取消预订消息处理接口，使用 ocpp.routing.on 装饰器注册对应接收消息的处理函数，
    # 该函数用于接收对应消息的消息体数据，并需要返回对应消息的应答数据结构体。
    @on(Action.CancelReservation)
    def on_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))

        # 当收到消息后，可以在此处进行业务功能的处理，
        # 或者先进行应答，然后再在 ocpp.routing.after 装饰的函数内进行业务处理。

        # 该函数必须返回对应消息的应答消息体，用于应答服务器消息
        return self._call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )
```

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|action|str|对应的消息类型，可以直接使用 `ocpp.vxx.enums.Actions` 枚举值中的数据|
|skip_schema_validation|bool|是否跳过请求或应答消息体数据校验<br>`True` - 跳过校验<br>`False` - 不跳过校验<br>默认：`False`|
|call_unique_id_required|bool|是否将消息唯一标识做为参数传入被装饰的函数<br>`True` - 是<br>`False` - 否<br>默认：`False`|

### <span id="routing-after">`ocpp.routing.after`</span>

- 该装饰器用于处理对应服务器下发消息的封装函数，其在 `ocpp.routing.on` 装饰的函数调用之后进行调用。
- 被装饰的函数入参为接收消息的数据结构信息，返回值无特殊要求

```python
class ChargePoint(cp):

    # 客户端在接收到取消预订消息后，在应答完成后或无需应答之后，需要进行的业务处理功能，
    # 可以使用 ocpp.routing.after 装饰器注册对应接收消息的处理函数。
    @after(Action.CancelReservation, call_unique_id_required=True)
    def after_cancel_reservation(self, reservation_id, call_unique_id):
        logger.info("reservation_id %s, call_unique_id %s" % (reservation_id, call_unique_id))
        # 可以在此处处理对应的业务功能，该函数对返回值无特殊要求
        return
```

**参数说明：**

|参数|类型|说明|
|:---|:---|:---|
|action|str|对应的消息类型，可以直接使用 `ocpp.vxx.enums.Actions` 枚举值中的数据|
|call_unique_id_required|bool|是否将消息唯一标识做为参数传入被装饰的函数<br>`True` - 是<br>`False` - 否<br>默认：`False`|

## 基于 `ChargePoint` 二次开发示例

- 该抽象类封装了基于 websocket 协议，需要实例化 `uwebsocket` 对象做为参数，进行 `ChargePoint` 模块的初始化；
- 使用时，从对应的版本中导入 `ChargePoint` 类，如：`from usr.ocpp.v16 import ChargePoint as cp`。

**注意：**

以下只分别列出了一个客户端发送消息和一个客户端接收消息的处理函数的示例做为参考，实际项目需要使用哪些请求消息和接收消息，需要根据项目的实际要求进行开发

```python
import utime
import _thread
# 导入 uwebsocket 模块，实例化对象，用于 ChargePoint 类。
from usr.tools import uwebsocket, logging
# 导入 v16 版本的 ChargePoint 做为项目基类
from usr.ocpp.v16 import ChargePoint as cp


# 基于 v16 版本的项目基类进行二次开发，封装需要用到的客户端发送接口和消息接收的接口
class ChargePoint(cp):

    # 客户端发送请求认证接口
    def send_authorize(self):
        # 使用 AuthorizePayload 类生成客户端请求认证接口的数据结构体
        request = self._call.AuthorizePayload(
            id_tag="xxx",
        )
        # 调用 call 方法发送消息并等待接收应答
        response = self.call(request)
        logger.info("response %s" % response)

        # 判断应答解析后是否为请求认证接口的应答数据结构体，是则进行应答数据的处理
        if isinstance(response, self._call_result.AuthorizePayload):
            logger.info("id_tag_info %s." % response.id_tag_info)

    # 客户端接收取消预订消息处理接口，使用 ocpp.routing.on 装饰器注册对应接收消息的处理函数，
    # 该函数用于接收对应消息的消息体数据，并需要返回对应消息的应答数据结构体。
    @on(Action.CancelReservation)
    def on_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))

        # 当收到消息后，可以在此处进行业务功能的处理，
        # 或者先进行应答，然后再在 ocpp.routing.after 装饰的函数内进行业务处理。

        # 该函数必须返回对应消息的应答消息体，用于应答服务器消息
        return self._call_result.CancelReservationPayload(
            status=CancelReservationStatus.accepted
        )

    # 客户端在接收到取消预订消息后，在应答完成后或无需应答之后，需要进行的业务处理功能，
    # 可以使用 ocpp.routing.after 装饰器注册对应接收消息的处理函数。
    @after(Action.CancelReservation)
    def after_cancel_reservation(self, reservation_id):
        logger.info("reservation_id %s" % (reservation_id))
        # 可以在此处处理对应的业务功能，该函数对返回值无特殊要求
        return

# 建议使用设备 IMEI 或设备 MAC 地址做为设备标识
IMEI = "XXXX"
# 对应服务器的 IP 地址
host = "xxx.xxx.xxx.xxx"
# 对应服务器的端口号
port = "xxxx"
# 实例化一个 uwebsocket 对象
ws = uwebsocket.Client.connect(
    "ws://{host}:{port}/{IMEI}",
    # 在 header 中添加对应的 OCPP 版本号用于服务端进行识别，不同的服务端有不同的要求，按实际的情况进行填写
    headers={"Sec-WebSocket-Protocol": "ocpp1.6.0"},
    debug=False
)

# 实例化二次开发的包含具体业务功能的 ChargePoint 对象
cp = ChargePoint(IMEI, ws)

# 启动一个线程用于接收服务器下发的数据
_thread.start_new_thread(cp.start, ())

# 发送请求认证消息
cp.send_authorize()

# 等待接收服务器数据
utime.sleep(10)
```
