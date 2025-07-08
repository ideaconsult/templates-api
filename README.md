# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/ideaconsult/templates-api/blob/COVERAGE-REPORT/htmlcov/index.html)

| Name                                     |    Stmts |     Miss |   Cover |   Missing |
|----------------------------------------- | -------: | -------: | ------: | --------: |
| src/tplapi/\_\_init\_\_.py               |        0 |        0 |    100% |           |
| src/tplapi/api/\_\_init\_\_.py           |        0 |        0 |    100% |           |
| src/tplapi/api/info.py                   |       13 |        2 |     85% |     16-17 |
| src/tplapi/api/tasks.py                  |       20 |       10 |     50% |     20-35 |
| src/tplapi/api/templates.py              |      224 |       74 |     67% |45-46, 59-60, 74, 79-81, 104-117, 129-147, 169-173, 238, 248, 262, 297-304, 341-374, 380-381, 384-385, 434-437, 442 |
| src/tplapi/api/utils.py                  |        7 |        0 |    100% |           |
| src/tplapi/config/\_\_init\_\_.py        |        0 |        0 |    100% |           |
| src/tplapi/config/app\_config.py         |       34 |        3 |     91% | 26-27, 33 |
| src/tplapi/main.py                       |       41 |       10 |     76% |35-44, 48-61, 65 |
| src/tplapi/models/\_\_init\_\_.py        |        0 |        0 |    100% |           |
| src/tplapi/models/models.py              |       17 |        0 |    100% |           |
| src/tplapi/services/template\_service.py |      148 |       49 |     67% |31-39, 45-46, 52-58, 68-70, 99-100, 103-104, 107-111, 124-148, 179-185, 239, 245-246 |
| tests/api\_template\_test.py             |      182 |        4 |     98% |52, 57, 107-108 |
| tests/api\_test.py                       |       31 |        0 |    100% |           |
|                                **TOTAL** |  **717** |  **152** | **79%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/ideaconsult/templates-api/COVERAGE-REPORT/badge.svg)](https://htmlpreview.github.io/?https://github.com/ideaconsult/templates-api/blob/COVERAGE-REPORT/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ideaconsult/templates-api/COVERAGE-REPORT/endpoint.json)](https://htmlpreview.github.io/?https://github.com/ideaconsult/templates-api/blob/COVERAGE-REPORT/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fideaconsult%2Ftemplates-api%2FCOVERAGE-REPORT%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/ideaconsult/templates-api/blob/COVERAGE-REPORT/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.