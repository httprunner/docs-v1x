## 介绍

在自动化测试中，经常会遇到如下场景：

> 1、测试搜索功能，只有一个搜索输入框，但有10种不同类型的搜索关键字；
> 2、测试账号登录功能，需要输入用户名和密码，按照等价类划分后有20种组合情况。

这里只是随意找了两个典型的例子，相信大家都有遇到过很多类似的场景。总结下来，就是在我们的自动化测试脚本中存在参数，并且我们需要采用不同的参数去运行。

经过概括，参数基本上分为两种类型：

- 单个独立参数：例如前面的第一种场景，我们只需要变换搜索关键字这一个参数
- 多个具有关联性的参数：例如前面的第二种场景，我们需要变换用户名和密码两个参数，并且这两个参数需要关联组合

然后，对于参数而言，我们可能具有一个参数列表，在脚本运行时需要按照不同的规则去取值，例如顺序取值、随机取值、循环取值等等。

这就是典型的参数化和数据驱动。

如需了解 HttpRunner 参数化数据驱动机制的实现原理和技术细节，可前往阅读[《HttpRunner 实现参数化数据驱动机制》][http://debugtalk.com/post/httprunner-data-driven/]。

## 使用说明

在 HttpRunner 中若要使用数据驱动，需要进行两步操作：参数定义和数据源准备。

### 参数定义

在 YAML/JSON 测试用例的 config 模块中，新增一个`parameters`字段，参数化的定义均放置在该字段下。

定义内容包括参数名称和参数取值方式。

- 独立参数单独进行定义；多个参数具有关联性的参数需要将其定义在一起，采用短横线（`-`）进行连接。
- 参数取值方式当前支持顺序取值（Sequential）和乱序取值（Random）两种方式。

示例如下：

```yaml
- config:
    name: "demo"
    parameters:
        - user_agent: Random
        - username-password: Sequential
```

假如测试用例中定义了多个参数，那么测试用例在运行时会对参数进行笛卡尔积组合，覆盖所有参数组合情况。

参数取值方式采用乱序取值（Random）时，会先对该参数进行乱序排序，然后再进行笛卡尔积组合。

### 数据源准备

约定采用`.csv`文件格式来存储参数列表，独立参数存放在独立的`.csv`文件中，多个具有关联性的参数存放在一个`.csv`文件中；文件名称需要与参数名称保持一致，多个具有关联性的参数采用短横线（`-`）进行连接。

同时，约定在`.csv`文件中的第一行必须为参数名称；从第二行开始为参数值，每个值占一行；参数名称和数值之间采用逗号进行分隔。

例如，`keyword`这种独立的参数就可以存放在`keyword.csv`中，内容形式如下：

```csv
keyword
hello
world
debugtalk
```

`username`和`password`这种具有关联性的参数就可以存放在`username-password.csv`中，内容形式如下：

```csv
username,password
test1,111111
test2,222222
test3,333333
```

### 参数化运行

完成以上参数定义和数据源准备工作之后，参数化运行与普通测试用例的运行完全一致。

采用 hrun 命令运行自动化测试：

```bash
$ hrun tests/data/demo_parameters.yml
```

采用 locusts 命令运行性能测试：

```bash
$ locusts -f tests/data/demo_parameters.yml
```

区别在于，测试用例集在运行时会分别运行每一种组合情况；自动化测试时遍历一遍后会终止执行，性能测试时每个用户都会循环遍历。

## 案例演示

假设我们有一个获取token的接口，我们需要使用 user_agent 和 app_version 这两个参数来进行参数化数据驱动。

YAML 测试用例的描述形式如下所示：

```yaml
- config:
    name: "user management testset."
    parameters:
        - user_agent: Random
        - app_version: Sequential
    variables:
        - user_agent: 'iOS/10.3'
        - device_sn: ${gen_random_string(15)}
        - os_platform: 'ios'
        - app_version: '2.8.6'
    request:
        base_url: $BASE_URL
        headers:
            Content-Type: application/json
            device_sn: $device_sn

- test:
    name: get token with $user_agent and $app_version
    api: get_token($user_agent, $device_sn, $os_platform, $app_version)
    extract:
        - token: content.token
    validate:
        - "eq": ["status_code", 200]
        - "len_eq": ["content.token", 16]
```

其中，user_agent 和 app_version 的数据源列表分别为：

```csv
user_agent
iOS/10.1
iOS/10.2
iOS/10.3
```

```csv
app_version
2.8.5
2.8.6
```

那么，经过笛卡尔积组合，应该总共有6种参数组合情况，并且 user_agent 为乱序取值，app_version 为顺序取值。

最终的测试结果如下所示：

```
$ hrun tests/data/demo_parameters.yml

Running tests...
----------------------------------------------------------------------
 get token with iOS/10.2 and 2.8.5 ... INFO:root: Start to POST http://127.0.0.1:5000/api/get-token
INFO:root: status_code: 200, response_time: 13 ms, response_length: 46 bytes
OK (0.014845)s
 get token with iOS/10.2 and 2.8.6 ... INFO:root: Start to POST http://127.0.0.1:5000/api/get-token
INFO:root: status_code: 200, response_time: 2 ms, response_length: 46 bytes
OK (0.003909)s
 get token with iOS/10.1 and 2.8.5 ... INFO:root: Start to POST http://127.0.0.1:5000/api/get-token
INFO:root: status_code: 200, response_time: 3 ms, response_length: 46 bytes
OK (0.004090)s
 get token with iOS/10.1 and 2.8.6 ... INFO:root: Start to POST http://127.0.0.1:5000/api/get-token
INFO:root: status_code: 200, response_time: 5 ms, response_length: 46 bytes
OK (0.006673)s
 get token with iOS/10.3 and 2.8.5 ... INFO:root: Start to POST http://127.0.0.1:5000/api/get-token
INFO:root: status_code: 200, response_time: 3 ms, response_length: 46 bytes
OK (0.004775)s
 get token with iOS/10.3 and 2.8.6 ... INFO:root: Start to POST http://127.0.0.1:5000/api/get-token
INFO:root: status_code: 200, response_time: 3 ms, response_length: 46 bytes
OK (0.004846)s
----------------------------------------------------------------------
Ran 6 tests in 0.046s
```
