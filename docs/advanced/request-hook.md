## 概述

HttpRunner 从 `1.4.3` 版本开始实现了全新的 hook 机制，可以在请求前和请求后调用钩子函数。

## 用例描述形式

在 YAML/JSON 测试用例中新增关键字 `setup_hooks` 和 `teardown_hooks`。

- setup_hooks: 在 HTTP 请求发送前执行 hook 函数，主要用于准备工作；甚至可以实现对请求的 request 内容进行预处理。
- teardown_hooks: 在 HTTP 请求发送后执行 hook 函数，主要用于测试后的清理工作。

```json
"test": {
    "name": "get token with $user_agent, $os_platform, $app_version",
    "request": {
        "url": "/api/get-token",
        "method": "POST",
        "headers": {
            "app_version": "$app_version",
            "os_platform": "$os_platform",
            "user_agent": "$user_agent"
        },
        "json": {
            "sign": "${get_sign($user_agent, $device_sn, $os_platform, $app_version)}"
        }
    },
    "validate": [
        {"eq": ["status_code", 200]}
    ],
    "setup_hooks": [
        "${setup_hook_prepare_kwargs($request)}",
        "${setup_hook_httpntlmauth($request)}"
    ],
    "teardown_hooks": [
        "${teardown_hook_sleep_N_secs($response, 2)}"
    ]
}
```

hook 函数的定义放置在项目的 debugtalk.py 中，在 YAML/JSON 中调用 hook 函数仍然是采用 ${func()} 的形式。

## 编写 hook 函数

### setup_hooks

setup_hooks 函数除了可传入自定义参数外，还可以传入 `$request`，该参数对应着当前测试用例的 request 全部内容。因为 request 是可变参数类型（dict），因此该函数参数为引用传递，当我们需要对请求参数进行预处理时尤其有用。

e.g.

```python
def setup_hook_prepare_kwargs(request):
    if request["method"] == "POST":
        content_type = request.get("headers", {}).get("content-type")
        if content_type and "data" in request:
            # if request content-type is application/json, request data should be dumped
            if content_type.startswith("application/json") and isinstance(request["data"], (dict, list)):
                request["data"] = json.dumps(request["data"])

            if isinstance(request["data"], str):
                request["data"] = request["data"].encode('utf-8')

def setup_hook_httpntlmauth(request):
    if "httpntlmauth" in request:
        from requests_ntlm import HttpNtlmAuth
        auth_account = request.pop("httpntlmauth")
        request["auth"] = HttpNtlmAuth(
            auth_account["username"], auth_account["password"])
```

### teardown_hooks

teardown_hooks 函数除了可传入自定义参数外，还可以传入 `$response`，该参数对应着当前 request 的响应实例（requests.Response）。

e.g.

```python
def teardown_hook_sleep_N_secs(response, n_secs):
    """ sleep n seconds after request
    """
    if response.status_code == 200:
        time.sleep(0.1)
    else:
        time.sleep(n_secs)
```
