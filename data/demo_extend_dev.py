from httprunner import HttpRunner

kwargs = {
    "failfast": False
}
result = HttpRunner("docs/data/demo-quickstart-2.yml", **kwargs).run(
    mapping={},
    html_report_name="demo"
)
print('result--', result)
