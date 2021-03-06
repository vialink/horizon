# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from horizon.test import helpers as test


class BrowserTests(test.SeleniumTestCase):
    def test_qunit(self):
        self.selenium.get("%s%s" % (self.live_server_url, "/qunit/"))
        wait = self.ui.WebDriverWait(self.selenium, 20)

        def qunit_done(driver):
            text = driver.find_element_by_id("qunit-testresult").text
            return "Tests completed" in text

        wait.until(qunit_done)
        failed = self.selenium.find_element_by_class_name("failed")
        if int(failed.text) > 0:
            filename = self.selenium.find_element_by_css_selector(
                "#qunit-tests > li.fail span.test-name").text
            message = self.selenium.find_element_by_css_selector(
                "#qunit-tests > li.fail span.test-message").text
            self.fail('%s: %s' % (filename, message))
