from selenium_ui.jsm import modules_agents
import pytest
from extension.jsm import extension_ui_agents  # noqa F401
from util.conf import JSM_SETTINGS


def is_dataset_small(jsm_datasets):
    return len(jsm_datasets[modules_agents.SERVICE_DESKS_MEDIUM]) == 0


# this action should be the first one
def test_0_selenium_agent_a_login(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.login(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_browse_projects(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.agent_browse_projects(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_view_customers(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.view_customers(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_view_request(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.view_request(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_view_report_workload_medium(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    if is_dataset_small(jsm_datasets):
        pytest.skip("Dataset does not have medium (10k-100k requests) service desk. Skipping action.")
    modules_agents.view_report_workload_medium(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_view_report_created_vs_resolved_medium(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    if is_dataset_small(jsm_datasets):
        pytest.skip("Dataset does not have medium (10k-100k requests) service desk. Skipping action.")
    modules_agents.view_report_created_vs_resolved_medium(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_view_report_workload_small(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.view_report_workload_small(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_view_report_created_vs_resolved_small(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.view_report_created_vs_resolved_small(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_add_comment(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.add_comment(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_view_queues_medium(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    if is_dataset_small(jsm_datasets):
        pytest.skip("Dataset does not have medium (10k-100k requests) service desk. Skipping action.")
    modules_agents.view_queues_medium(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_view_queues_small(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.view_queues_small(jsm_webdriver, jsm_datasets)


"""
Add custom actions anywhere between login and log out action. Move this to a different line as needed.
Write your custom selenium scripts in `app/extension/jsm/extension_ui_agents.py`.
Refer to `app/selenium_ui/jsm/modules_agents.py` for examples.
"""
# def test_1_selenium_agent_custom_action(jsm_webdriver, jsm_datasets, jsm_screen_shots):
#     extension_ui_agents.app_specific_action(jsm_webdriver, jsm_datasets)

def test_1_selenium_create_dashboard(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_create_dashboard(jira_webdriver, jira_datasets)


def test_1_selenium_add_performance_objectives_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'performance-objectives', True, False, False, False)

def test_1_selenium_add_performance_trend_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'performance-trend', False, False, False, False)

def test_1_selenium_add_circular_chart_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'circle', False, False, False, False)

def test_1_selenium_add_multi_metric_combined_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'multi-metric-bar', False, True, False, False)

def test_1_selenium_add_multi_metric_trend_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'multi-metric-trend', False, True, False, False)    

def test_1_selenium_add_change_history_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'change-history', False, False, True, False)

def test_1_selenium_add_performance_treemap_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'tree-map', False, False, False, False)

def test_1_selenium_add_performance_heatmap_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'heat-map', False, False, False, True)

def test_1_selenium_add_performance_venn_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'venn', False, False, False, False)

def test_1_selenium_add_performance_scatter_bubble_gadget(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_gadget(jira_webdriver, jira_datasets, 'scatter-bubble', False, False, False, False)

def test_1_selenium_delete_dashboard(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_delete_dashboard(jira_webdriver, jira_datasets)

def test_1_selenium_add_calendar(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_add_remove_work_calendar(jira_webdriver, jira_datasets)

def test_1_selenium_change_color_palette(jira_webdriver, jira_datasets, jira_screen_shots):
    extension_ui_agents.app_change_color_palette(jira_webdriver, jira_datasets)

"""
To enable specific tests for Insight below, set 'True' next to `insight` variable (False by default) in  `app/jsm.yml`
"""


def test_1_selenium_agent_insight_main_page(jsm_webdriver, jsm_datasets, jira_screen_shots):
    if not JSM_SETTINGS.insight:
        pytest.skip()
    modules_agents.insight_main_page(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_insight_create_new_schema(jsm_webdriver, jsm_datasets, jira_screen_shots):
    if not JSM_SETTINGS.insight:
        pytest.skip()
    modules_agents.insight_create_new_schema(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_insight_create_new_object(jsm_webdriver, jsm_datasets, jira_screen_shots):
    if not JSM_SETTINGS.insight:
        pytest.skip()
    modules_agents.insight_create_new_object(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_insight_delete_new_schema(jsm_webdriver, jsm_datasets, jira_screen_shots):
    if not JSM_SETTINGS.insight:
        pytest.skip()
    modules_agents.insight_delete_new_schema(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_insight_view_queue_with_insight_column(jsm_webdriver, jsm_datasets, jira_screen_shots):
    if not JSM_SETTINGS.insight:
        pytest.skip()
    modules_agents.insight_view_queue_insight_column(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_insight_search_object_by_iql(jsm_webdriver, jsm_datasets, jira_screen_shots):
    if not JSM_SETTINGS.insight:
        pytest.skip()
    modules_agents.insight_search_object_by_iql(jsm_webdriver, jsm_datasets)


def test_1_selenium_agent_insight_view_issue_with_objects(jsm_webdriver, jsm_datasets, jira_screen_shots):
    if not JSM_SETTINGS.insight:
        pytest.skip()
    modules_agents.view_issue_with_insight_objects(jsm_webdriver, jsm_datasets)


# this action should be the last one
def test_2_selenium_agent_z_logout(jsm_webdriver, jsm_datasets, jsm_screen_shots):
    modules_agents.logout(jsm_webdriver, jsm_datasets)
