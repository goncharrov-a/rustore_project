import allure


def owner(name: str):
    return allure.label("owner", name)


def layer(name: str):
    return allure.label("layer", name)


def component(name: str):
    return allure.label("component", name)


def microservice(name: str):
    return allure.label("msrv", name)


def tm4j(case_id: str):
    return allure.label("tm4j", case_id)


def jira_issues(*issues: str):
    return allure.label("jira", *issues)
