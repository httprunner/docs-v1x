## 运行环境

HttpRunner 是一个基于 Python 开发的测试框架，可以运行在 macOS、Linux、Windows 系统平台上。

HttpRunner 的开发环境为 macOS + Python 3.6；实际上，HttpRunner 支持 Python 2.7 和 Python 3.3 以上的所有版本，并使用 Travis-CI 进行了[持续集成测试][travis-ci]，测试覆盖的版本包括 2.7/3.4/3.5/3.6。

推荐使用 macOS/Linux + Python 3.6 的运行环境组合。

## 安装方式

HttpRunner 的稳定版本托管在 PyPI 上，可以使用`pip`或者`easy_install`进行安装。

```bash
$ pip install httprunner
```

或者

```bash
$ easy_install httprunner
```

如果你需要使用最新的开发版本，那么可以采用项目的 GitHub 仓库地址进行安装：

```bash
$ pip install git+https://github.com/HttpRunner/HttpRunner.git#egg=HttpRunner
```

## 版本升级

假如你之前已经安装过了 HttpRunner，现在需要升级到最新版本，那么你可以使用`-U`参数。该参数对以上三种安装方式均生效。

```bash
$ pip install -U HttpRunner
$ easy_install -U HttpRunner
$ pip install -U git+https://github.com/HttpRunner/HttpRunner.git#egg=HttpRunner
```

## 安装校验

在 HttpRunner 安装成功后，在你的系统中会新增如下 4 个命令：

- httprunner: 核心命令
- hrun: httprunner 的缩写，功能与 httprunner 完全相同
- ate: 曾经用过的命令（当时框架名称为 ApiTestEngine），功能与 httprunner 完全相同
- locusts: 用于[性能测试](load-test.md)

httprunner、hrun、ate 三个命令完全等价，功能特性完全相同，个人推荐使用`hrun`命令。

运行如下命令，若正常显示版本号，则说明 HttpRunner 安装成功。

```bash
$ hrun -V
HttpRunner version: 0.9.0
PyUnitReport version: 0.1.4
```

<!-- ## 使用 docker 镜像 -->

[travis-ci]: https://travis-ci.org/HttpRunner/HttpRunner