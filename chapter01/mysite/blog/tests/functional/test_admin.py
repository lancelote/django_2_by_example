class TestPostAdmin:

    def test_displayed_list(self, post_factory, admin, browser, live_server):
        # We have two posts
        post1 = post_factory(author=admin)
        post2 = post_factory(author=admin)

        # Admin opens admin panel
        browser.get(live_server.url + '/admin')

        # Admin checks page title to be sure he is in the right place
        assert browser.title == 'Log in | Django site admin'

        # Admin logs in
        browser.login('admin', 'password')

        # Admin sees a link to Posts
        posts_link = browser.find_element_by_link_text('Posts')
        assert posts_link.get_attribute('href') == live_server.url + '/admin/blog/post/'

        # Admin clicks on a Posts link and see table of posts with columns: title, slug, author, publish and status
        posts_link.click()
        assert browser.find_element_by_css_selector('.column-title a').text == 'TITLE'
        assert browser.find_element_by_css_selector('.column-slug a').text == 'SLUG'
        assert browser.find_element_by_css_selector('.column-author a').text == 'AUTHOR'
        assert browser.find_element_by_css_selector('.column-publish .text a').text == 'PUBLISH'
        assert browser.find_element_by_css_selector('.column-status .text a').text == 'STATUS'

        # Admin can filter by status, created date and publish date
        filter_div = browser.find_element_by_id('changelist-filter')
        filter_options = filter_div.find_elements_by_tag_name('h3')
        assert filter_options[0].text == 'By status'
        assert filter_options[1].text == 'By created'
        assert filter_options[2].text == 'By publish'

        # Admin can search by post title and body
        assert len(browser.search_model_by('')) == 2
        assert len(browser.search_model_by(post1.title)) == 1
        assert len(browser.search_model_by(post2.title)) == 1
        assert len(browser.search_model_by('Unknown Post')) == 0

        # Admin can see the date hierarchy links by publish date
        browser.find_element_by_class_name('xfull')

        # Posts shorted by status and than by publish date
        browser.search_model_by('')
        assert browser.find_element_by_css_selector('th:last-child span').text == '1'
        assert browser.find_element_by_css_selector('th:nth-child(5) span').text == '2'


# class TestModelAdmin(StaticLiveServerTestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Firefox()
#         self.admin_user = get_user_model().objects.create_superuser(
#             username='admin',
#             email='admin@example.com',
#             password='password'
#         )
#
#     def tearDown(self):
#         self.browser.quit()
#
#     def search_model_by(self, text):
#         search_field = self.browser.find_element_by_id('searchbar')
#         search_button = self.browser.find_element_by_css_selector('#changelist-search input[type="submit"]')
#
#         search_field.clear()
#         search_field.send_keys(text)
#         search_button.click()
#
#         return self.browser.find_elements_by_css_selector('#result_list [class^="row"]')
#
#
# @pytest.mark.skip
# class TestPostAdmin(TestModelAdmin):
#
#     def test_displayed_list(self):
#         # We have two posts
#         post1 = PostFactory(author=self.admin_user)
#         post2 = PostFactory(author=self.admin_user)
#
#         # Admin opens admin panel
#         self.browser.get(self.live_server_url + '/admin/')
#
#         # He checks page title to be sure he is in the right place
#         self.assertEqual(self.browser.title, 'Log in | Django site admin')
#
#         # He logs in
#         login(self.browser, 'admin', 'password')
#
#         # He sees link to Posts
#         posts_link = self.browser.find_element_by_link_text('Posts')
#         self.assertEqual(posts_link.get_attribute('href'), self.live_server_url + '/admin/blog/post/')
#
#         # He clicks on Posts link and see table of posts with columns: title, slug, author, publish and status
#         posts_link.click()
#         self.assertEqual(self.browser.find_element_by_css_selector('.column-title a').text, 'TITLE')
#         self.assertEqual(self.browser.find_element_by_css_selector('.column-slug a').text, 'SLUG')
#         self.assertEqual(self.browser.find_element_by_css_selector('.column-author a').text, 'AUTHOR')
#         self.assertEqual(self.browser.find_element_by_css_selector('.column-publish .text a').text, 'PUBLISH')
#         self.assertEqual(self.browser.find_element_by_css_selector('.column-status .text a').text, 'STATUS')
#
#         # He can filter by status, created date and publish date
#         filter_div = self.browser.find_element_by_id('changelist-filter')
#         filter_options = filter_div.find_elements_by_tag_name('h3')
#         self.assertEqual(filter_options[0].text, 'By status')
#         self.assertEqual(filter_options[1].text, 'By created')
#         self.assertEqual(filter_options[2].text, 'By publish')
#
#         # He can search by post title and body
#         self.assertEqual(len(self.search_model_by('')), 2)
#         self.assertEqual(len(self.search_model_by(post1.title)), 1)
#         self.assertEqual(len(self.search_model_by(post2.title)), 1)
#         self.assertEqual(len(self.search_model_by('Unknown Post')), 0)
#
#         # He can see the date hierarchy links by publish date
#         self.browser.find_element_by_class_name('xfull')
#
#         # Posts sorted by status and than by publish date
#         self.search_model_by('')
#         self.assertEqual(self.browser.find_element_by_css_selector('th:last-child span').text, '1')
#         self.assertEqual(self.browser.find_element_by_css_selector('th:nth-child(5) span').text, '2')
#
#         # He start a new post
#         self.browser.find_element_by_css_selector('.addlink').click()
#
#         # He types in post title
#         self.browser.find_element_by_id('id_title').send_keys('Hello World')
#
#         # He sees that slug field auto-updates
#         self.assertEqual(self.browser.find_element_by_id('id_slug').get_attribute('value'), 'hello-world')
#
#         # He click at the author lookup button
#         self.browser.find_element_by_id('lookup_id_author').click()
#         self.browser.switch_to.window(self.browser.window_handles[1])
#
#         # He choose author
#         self.browser.find_element_by_css_selector('.row1 a').click()
#
#         # He sees that author correctly selected
#         self.browser.switch_to.window(self.browser.window_handles[0])
#         self.assertEqual(self.browser.find_element_by_id('id_author').get_attribute('value'), str(self.admin_user.id))
#
#         # He types in the post body
#         self.browser.find_element_by_id('id_body').send_keys('Sample post body')
#
#         # He sees publish section
#         self.browser.find_element_by_id('id_publish_0')
#
#         # He switch post status to Published
#         select = Select(self.browser.find_element_by_id('id_status'))
#         select.select_by_visible_text('Published')
#
#         # Saves the post
#         self.browser.find_element_by_css_selector('.submit-row .default').click()
#
#         # And he sees a new post in the list
#         self.assertEqual(len(self.search_model_by('')), 3)
