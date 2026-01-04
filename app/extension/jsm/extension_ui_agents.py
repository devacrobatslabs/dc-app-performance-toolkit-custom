import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jsm.pages.agent_pages import Login
from util.conf import JSM_SETTINGS



def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action

    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.set_credentials(username=username, password=password)
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_agent_app_custom_action")
    def measure():

        @print_timing("selenium_agent_app_custom_action:view_request")
        def sub_measure():
            page.go_to_url(f"{JSM_SETTINGS.server_url}/browse/{issue_key}")
            # Wait for summary field visible
            page.wait_until_visible((By.ID, "summary-val"))
            # Wait for you app-specific UI element by ID selector
            page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))
        sub_measure()
    measure()

def app_create_dashboard(jira_webdriver, jira_datasets):
    page = BasePage(jira_webdriver)
    @print_timing("selenium_create_board")
    def measure():
        dashboardTitle = f"My Dashboard {time.time()}"
        page.go_to_url(f"{JSM_SETTINGS.server_url}/secure/ConfigurePortalPages.jspa")
        page.wait_until_visible((By.ID, "main"))
        close_info_popups(page) # just in case of popups

        try:
           page.get_element((By.ID,'create_page')).click()
        except:
            close_info_popups(page)
            page.get_element((By.ID,'create_page')).click()

        admin_login_prompt(page)
        page.wait_until_clickable((By.ID, 'edit-entity-dashboard-name')).send_keys(dashboardTitle)
        page.get_element((By.ID,'edit-entity-submit')).click()
        page.get_element((By.XPATH, f'//table//td//a[contains(.,\'{dashboardTitle}\')]')).click() # navigate to the new dashboard
        page.wait_until_visible((By.ID, "dashboard"))
        close_info_popups(page) # just in case of popups
    measure()

# def load_more_items(jira_webdriver):
#     page.wait_until_visible((By.ID,'message-panel'))
#     try:
#         page.wait_until_visible((By.ID,'load-more-directory-items')).click()
#     except:
#         print('Already loaded')
        

def app_add_gadget(jira_webdriver, jira_datasets, gadgetId, isLoadMore, isMulti, isHistory, isHeat):
    page = BasePage(jira_webdriver)
    close_info_popups(page);
    gadgetPath = f'//div[@class=\'aui-dialog2-content\']//button[contains(@data-item-id,\'performance-objectives-for-jira:{gadgetId}\')]'
    testName = f'selenium_app_add_gadget_{gadgetId}' 
    @print_timing(testName)
    def measure():
        dsName = 'This week'
        PROJECT_KEY = 'TESTAUTO'
        JQL_HISTORY=f'key={PROJECT_KEY}-1'
        JQL_PROJECT=f'project={PROJECT_KEY}'
        NUMBER_OF_ISSUES = 'Number of issues'
        RESOLUTION = 'Resolution'
        ORIGINAL_ESTIMATE = 'Original Estimate'

        @print_timing(f'{testName}: add gadget')
        def sub_measure():
            try:
               page.get_element((By.ID,'add-gadget')).click()
            except:
               close_info_popups(page)
               page.wait_until_clickable((By.ID,'add-gadget')).click()
            
            page.wait_until_visible((By.ID,'list-panel'))
            
            try:
                page.get_element((By.XPATH, gadgetPath)).click()
            except:
                page.wait_until_visible((By.ID,'load-more-directory-items')).click()
                page.wait_until_visible((By.XPATH, gadgetPath)).click()

            page.wait_until_clickable((By.CSS_SELECTOR, '.aui-dialog2-header  button.aui-close-button')).click()
        sub_measure()

        @print_timing(f'{testName}: init')
        def sub_measure():
            page.wait_until_invisible((By.CSS_SELECTOR, '.aui-dialog2-header'))
            page.driver.switch_to.frame(page.wait_until_visible((By.CSS_SELECTOR,'.dashboard-item-content iframe')))
        sub_measure()

        try:
            @print_timing(f'{testName}: configure data source')
            def sub_measure():
                page.wait_until_clickable((By.ID, 'data-set-name')).send_keys(dsName)
                page.wait_until_clickable((By.ID, 'predefined-period')).click()
                page.wait_until_visible((By.CSS_SELECTOR, '.MuiMenu-list li[data-value=\'thisWeek\']'))
                page.wait_until_clickable((By.CSS_SELECTOR, '.MuiMenu-list li[data-value=\'thisWeek\']')).click()
                
                if page.get_elements((By.CSS_SELECTOR, '.MuiMenu-list')):
                    try:
                        page.wait_until_invisible((By.CSS_SELECTOR, '.MuiMenu-list')) # important other wise backdrop takes next click
                    except:
                        pass

                if page.get_elements((By.CSS_SELECTOR, '.MuiBackdrop-invisible')):
                    try:
                        page.get_element((By.CSS_SELECTOR, '.MuiBackdrop-invisible')).click()
                        page.wait_until_invisible((By.CSS_SELECTOR, '.MuiBackdrop-invisible')) # important other wise backdrop takes next click
                    except:
                        pass

                try: #first click may click the backdrop of the open select box
                   page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModal__Content label[for=\'textarea-jql\']')).click()
                except: #retry
                   try:
                      page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModal__Content label[for=\'textarea-jql\']')).click() 
                   except: #retry 
                      page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModal__Content label[for=\'textarea-jql\']')).click() 

                
                if isHistory:
                    page.wait_until_clickable((By.ID,'textarea-jql')).send_keys(JQL_HISTORY)
                else:
                    page.wait_until_clickable((By.ID,'textarea-jql')).send_keys(JQL_PROJECT)    

                try:
                    page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModalPortal .maui-button.primary')).click()
                except ElementClickInterceptedException: #retry 1 time because of loading disabled state
                    page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModalPortal .maui-button.primary')).click()

                page.wait_until_visible((By.CSS_SELECTOR,'.data-set-item-name'))
            sub_measure()
        
            @print_timing(f'{testName}: configure general')
            def sub_measure():
                if isMulti:
                    page.wait_until_clickable((By.CSS_SELECTOR, '.button-add-metric')).click()
                    page.wait_until_clickable((By.ID, 'metric-filters-picker')).click()
                    page.wait_until_clickable((By.ID, 'metric-filters-picker')).send_keys(NUMBER_OF_ISSUES)
                    page.wait_until_visible((By.CSS_SELECTOR, f'.MuiAutocomplete-listbox li[title=\'{NUMBER_OF_ISSUES}\']')).click()
                    page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModal__Content .maui-button.primary')).click()
                    page.wait_until_visible((By.CSS_SELECTOR, '.multi-metric-item'))
                if isHeat:
                    page.wait_until_clickable((By.CSS_SELECTOR, '.group-by button[title=\'Edit\']')).click()
                    page.wait_until_clickable((By.ID, 'field-picker')).click()
                    page.wait_until_clickable((By.ID, 'field-picker')).send_keys(RESOLUTION)
                    page.wait_until_clickable((By.CSS_SELECTOR, f'.MuiAutocomplete-listbox li[title*=\'{RESOLUTION}\']')).click()
                    page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModal__Content .maui-button.primary')).click()
                    page.wait_until_invisible((By.CSS_SELECTOR, '.ReactModal__Content'))
                if isHistory:
                    page.wait_until_clickable((By.CSS_SELECTOR, '.metric.single button')).click()
                    page.wait_until_clickable((By.ID, 'metric-filters-picker')).click()
                    page.wait_until_clickable((By.ID, 'metric-filters-picker')).send_keys(ORIGINAL_ESTIMATE)
                    page.wait_until_clickable((By.CSS_SELECTOR, f'.MuiAutocomplete-listbox li[title=\'{ORIGINAL_ESTIMATE}\']')).click()
                    page.wait_until_clickable((By.CSS_SELECTOR, '.ReactModal__Content .maui-button.primary')).click()
                    page.wait_until_invisible((By.CSS_SELECTOR, '.ReactModal__Content'))
            sub_measure()

            @print_timing(f'{testName}: save config')
            def sub_measure():
                page.wait_until_invisible((By.CSS_SELECTOR, '.ReactModal__Overlay'))
                page.wait_until_clickable((By.XPATH, '//button[text()[contains(.,\'Save\')]]')).click()
                # page.wait_until_invisible((By.CSS_SELECTOR,'button.maui-button.primary.wide'))
            sub_measure()

            @print_timing(f'{testName}: load chart')
            def sub_measure():
                page.wait_until_visible((By.CSS_SELECTOR,'.chart-footer'))        
            sub_measure()
        finally:
            @print_timing(f'{testName}: delete gadget')
            def sub_measure():
                page.driver.switch_to.parent_frame()
                page.wait_until_clickable((By.CSS_SELECTOR, '.gadget-menu button.aui-dd-trigger')).click()
                page.wait_until_clickable((By.CSS_SELECTOR, '.gadget-menu .dropdown-item .delete')).click()
                page.driver.switch_to.alert.accept()
                page.driver.switch_to.default_content()
                page.wait_until_visible((By.CSS_SELECTOR, '.column.first.empty'))
            sub_measure()
    measure()


def app_add_remove_work_calendar(jira_webdriver, datasets):
    page = BasePage(jira_webdriver) # /secure/ObjectivesWorkCalendarsAction!default.jspa
    @print_timing("selenium_app_add_remove_work_calendar")
    def measure():
        calendarName = f"Cal {time.time()}"  # the input field is ax length 25
        # navigate to calendar page
        page.go_to_url(f"{JSM_SETTINGS.server_url}/secure/ObjectivesWorkCalendarsAction!default.jspa")

        try:
            page.wait_until_clickable((By.ID, 'username-field')).send_keys(JSM_SETTINGS.admin_login)
            page.wait_until_clickable((By.ID, 'password-field'))
            page.get_element((By.ID, 'password-field')).send_keys(JSM_SETTINGS.admin_password)
            page.get_element((By.ID, 'login-button')).click()
        except:
            pass

        try:
            page.wait_until_visible((By.ID, 'login-form'))
            page.get_element((By.ID, 'login-form-authenticatePassword')).send_keys(JSM_SETTINGS.admin_password)
            page.get_element((By.ID, 'login-form-submit')).click()
        except:
            pass
        # add calendar
        page.wait_until_visible((By.CSS_SELECTOR, '.po-page'))
        page.wait_until_clickable((By.CSS_SELECTOR, 'button[title=\'Add calendar\']')).click()
        page.wait_until_clickable((By.ID, 'calendar-name')).send_keys(calendarName)
        page.get_element((By.CSS_SELECTOR, 'div[class^=\'ReactModal\'] button.maui-button.primary.wide')).click()
        page.wait_until_invisible((By.ID, 'calendar-name'))
        # delete calendar

        calPath = f'//div[@class=\'list-section\']//div[@class=\'row with-controls\']//span[text()[contains(.,\'{calendarName}\')]]/../..//button[@title=\'Delete\']'
        page.wait_until_visible((By.XPATH, calPath));
        page.get_element((By.XPATH, calPath)).click()
        page.get_element((By.CSS_SELECTOR, '.maui-button.primary.red')).click()
        page.wait_until_visible((By.CSS_SELECTOR, 'button[title=\'Add calendar\']'))
    measure()

def app_change_color_palette(jira_webdriver, datasets):
    page = BasePage(jira_webdriver) # /secure/ObjectivesWorkCalendarsAction!default.jspa
    @print_timing("selenium_app_change_color_palette")
    def measure():
        # navigate to color palette page
        page.go_to_url(f"{JSM_SETTINGS.server_url}/secure/ObjectivesColorPaletteAction!default.jspa")
        # change color pallete theme
        # Already logged as admin from work calendar
        # try:
        #     page.wait_until_clickable((By.ID, 'username-field')).send_keys(JSM_SETTINGS.admin_login)
        #     page.wait_until_clickable((By.ID, 'password-field'))
        #     page.get_element((By.ID, 'password-field')).send_keys(JSM_SETTINGS.admin_password)
        #     page.get_element((By.ID, 'login-button')).click()
        # except:
        #     pass

        try:
            page.wait_until_visible((By.ID, 'login-form'))
            page.get_element((By.ID, 'login-form-authenticatePassword')).send_keys(JSM_SETTINGS.admin_password)
            page.get_element((By.ID, 'login-form-submit')).click()
        except:
            pass

        page.wait_until_visible((By.CSS_SELECTOR, '.po-page'))
        page.wait_until_clickable((By.CSS_SELECTOR, '.header-link[aria-label*=\'Atlas\']')).click()
        page.get_element((By.CSS_SELECTOR, '.color-palette button.maui-button.primary')).click()
        page.wait_until_invisible((By.ID, '.color-palette .list-section'))
    measure()
    

def app_delete_dashboard(jira_webdriver, jira_datasets):
    page = BasePage(jira_webdriver)
    @print_timing("selenium_delete_board")
    def measure():
        page.wait_until_visible((By.CSS_SELECTOR,'#dash-options a.aui-dropdown2-trigger'))
        page.get_element((By.CSS_SELECTOR, '#dash-options a.aui-dropdown2-trigger')).click()  # Wait dashboadr list is visible
        close_info_popups(page)  # otherwise can't click on #delete_dashboard
        try: 
            page.wait_until_visible((By.ID,'delete_dashboard'))
            page.get_element((By.ID,'delete_dashboard')).click()  # click().perform()

            page.wait_until_visible((By.ID,'delete-portal-page-submit'))
            page.get_element((By.ID, 'delete-portal-page-submit')).click()
            page.wait_until_invisible((By.CSS_SELECTOR, '.jira-dialog'))
        except:
            pass
    measure()

def close_info_popups(page):
    try:
        clickList = page.get_elements((By.CSS_SELECTOR, '.closeable button'))
        if clickList:
            for clickEl in clickList:
                clickEl.click()
            page.wait_until_invisible((By.CSS_SELECTOR, '.closeable'))
    except:
        pass

def close_info_popups(page):
    try:
        clickList = page.get_elements((By.CSS_SELECTOR, '#theme-switcher-discovery-card button'))
        if clickList:
            for clickEl in clickList:
                clickEl.click()
            page.wait_until_invisible((By.CSS_SELECTOR, '#theme-switcher-discovery-card'))
    except:
        pass
    

    try:
        clickList = page.get_elements((By.CSS_SELECTOR, '.jira-help-tip button'))
        if clickList:
            for clickEl in clickList:
                clickEl.click()
            page.wait_until_invisible((By.CSS_SELECTOR, '.jira-help-tip'))
    except:
        pass

    try:
        clickList = page.get_elements((By.CSS_SELECTOR, '.insiders-signup-form .cancel'))
        if clickList:   # empty array is false in python
            for clickEl in clickList:
                clickEl.click()
            page.wait_until_invisible((By.CSS_SELECTOR, '.insiders-signup-form'))
    except:
        pass


    try:
        clickList = page.get_elements((By.CSS_SELECTOR, '.jira-help-tip .helptip-close'))
        if clickList:
            for clickEl in clickList:
                clickEl.click()
            page.wait_until_invisible((By.CSS_SELECTOR, '.jira-help-tip'))
    except:
        pass


def admin_login_prompt(page):
    try:
        login_prompt = page.get_elements((By.ID, 'username-field'))
        if login_prompt:
            page.wait_until_clickable((By.ID, 'username-field')).send_keys(JSM_SETTINGS.admin_login)
            page.wait_until_clickable((By.ID, 'password-field'))
            page.get_element((By.ID, 'password-field')).send_keys(JSM_SETTINGS.admin_password)
            page.get_element((By.ID, 'login-button')).click()
            page.get_element((By.ID, 'login-form-authenticatePassword')).send_keys(JSM_SETTINGS.admin_password)
            page.get_element((By.ID, 'login-form-submit')).click()
    except:
        print('Err closing')
