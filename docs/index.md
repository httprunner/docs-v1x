
HttpRunner 是一款面向 HTTP(S) 协议的通用测试框架，只需编写维护一份`YAML/JSON`脚本，即可实现自动化测试、性能测试、线上监控、持续集成等目的。

## 设计理念

- 充分复用优秀的开源项目，功能简洁但不简单
- 遵循`约定大于配置`的准则，将最佳工程实践融入其中
- 追求投入产出比，一份投入即可实现多种测试需求

## 核心特性

- 继承 [Requests][Requests] 的全部特性，轻松实现 HTTP(S) 的测试描述
- 测试用例与代码分离，采用`YAML/JSON`的形式描述测试场景
- 测试用例支持分层机制，充分实现测试用例的复用
- 测试用例支持参数化和数据驱动机制
- 使用 skip 机制实现对测试用例的分组执行控制
- 支持热加载机制，在文本测试用例中轻松实现复杂的定制化功能
- 基于 HAR 实现接口录制和用例生成功能（[har2case]）
- 结合 [Locust][Locust] 框架，无需额外的工作即可实现分布式性能测试
- 执行方式采用 CLI 调用，可与 Jenkins 等持续集成工具完美结合
- 测试结果统计报告简洁清晰，附带详尽统计信息和日志记录
- 具有可扩展性，便于扩展实现Web平台化（[HttpRunnerManager][HttpRunnerManager]）


[Requests]: http://docs.python-requests.org/en/master/
[Locust]: http://locust.io/
[har2case]: https://github.com/HttpRunner/har2case
[HttpRunnerManager]: https://github.com/HttpRunner/HttpRunnerManager