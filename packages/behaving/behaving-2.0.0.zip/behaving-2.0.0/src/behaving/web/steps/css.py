from behave import step
from .basic import _retry


@step(u'the element with xpath "{xpath}" should have the class "{cls}"')
def element_with_xpath_should_have_class(context, xpath, cls):
    element = context.browser.find_by_xpath(xpath)
    assert element, u"Element not found"
    assert element.first.has_class(cls), u"Class is not present on element"


@step(
    u'the element with xpath "{xpath}" should have the class "{cls}" within {timeout:d} seconds'
)
def element_by_xpath_should_have_class_within_timeout(context, xpath, cls, timeout):
    element = context.browser.find_by_xpath(xpath)
    assert element, u"Element not found"
    element = element.first
    check = lambda: element.has_class(cls)
    assert _retry(check, timeout), u"Class is not present on element"


@step(u'the element with xpath "{xpath}" should not have the class "{cls}"')
def element_with_xpath_should_not_have_class(context, xpath, cls):
    element = context.browser.find_by_xpath(xpath)
    assert element, u"Element not found"
    assert not element.first.has_class(cls), u"Class is present on element"


@step(
    u'the element with xpath "{xpath}" should not have the class "{cls}" within {timeout:d} seconds'
)
def element_by_xpath_should_not_have_class_within_timeout(context, xpath, cls, timeout):
    element = context.browser.find_by_xpath(xpath)
    assert element, u"Element not found"
    element = element.first
    check = lambda: not element.has_class(cls)
    assert _retry(check, timeout), u"Class is present on element"


@step(u'"{name}" should have the class "{cls}"')
def element_should_have_class(context, name, cls):
    element = context.browser.find_by_xpath(
        ("//*[@id='%(name)s']|" "//*[@name='%(name)s']") % {"name": name}
    )
    assert element, u"Element not found"
    assert element.first.has_class(cls), u"Class is not present on element"


@step(u'"{name}" should have the class "{cls}" within {timeout:d} seconds')
def element_should_have_class_within_timeout(context, name, cls, timeout):
    element = context.browser.find_by_xpath(
        ("//*[@id='%(name)s']|" "//*[@name='%(name)s']") % {"name": name}
    )
    assert element, u"Element not found"
    element = element.first
    check = lambda: element.has_class(cls)
    assert _retry(check, timeout), u"Class is not present on element"


@step(u'"{name}" should not have the class "{cls}"')
def element_should_not_have_class(context, name, cls):
    element = context.browser.find_by_xpath(
        ("//*[@id='%(name)s']|" "//*[@name='%(name)s']") % {"name": name}
    )
    assert element, u"Element not found"
    assert not element.first.has_class(cls), u"Class is present on element"


@step(u'"{name}" should not have the class "{cls}" within {timeout:d} seconds')
def element_should_have_class_within_timeout(context, name, cls, timeout):
    element = context.browser.find_by_xpath(
        ("//*[@id='%(name)s']|" "//*[@name='%(name)s']") % {"name": name}
    )
    assert element, u"Element not found"
    element = element.first
    check = lambda: not element.has_class(cls)
    assert _retry(check, timeout), u"Class is present on element"


@step(u'I should see an element with the css selector "{css}"')
def should_see_element_with_css(context, css):
    assert context.browser.is_element_present_by_css(css), u"Element not found"


@step(u'I should not see an element with the css selector "{css}"')
def should_not_see_element_with_css(context, css):
    assert context.browser.is_element_not_present_by_css(css), u"Element was found"


@step(
    u'I should see an element with the css selector "{css}" within {timeout:d} seconds'
)
def should_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_present_by_css(
        css, wait_time=timeout
    ), u"Element not found"


@step(
    u'I should not see an element with the css selector "{css}" within {timeout:d} seconds'
)
def should_not_see_element_with_css_within_timeout(context, css, timeout):
    assert context.browser.is_element_not_present_by_css(
        css, wait_time=timeout
    ), u"Element was found"


@step(u'I should see {n:d} elements with the css selector "{css}"')
def should_see_n_elements_with_css(context, n, css):
    element_list = context.browser.find_by_css(css)
    list_length = len(element_list)
    assert list_length == n, u"Found {list_length} elements, expected {n}".format(
        list_length, n
    )


@step(
    u'I should see at least {n:d} elements with the css selector "{css}" within {timeout:d} seconds'
)
def should_see_at_least_n_elements_with_css_within_timeout_seconds(
    context, n, css, timeout
):
    def _check():
        element_list = context.browser.find_by_css(css)
        list_length = len(element_list)
        return list_length >= n

    assert _retry(_check, timeout), "Did not find %s elements within %s seconds" % (
        n,
        timeout,
    )


###
# The following steps take element visibility into consideration (useful for testing SPAs).
###


def find_visible_by_css(context, css):
    """ Finds visible elements using a CSS selector. """
    return [elem for elem in context.browser.find_by_css(css) if elem.visible]


def _element_should_be_visible(context, css, timeout):
    check = lambda: len(find_visible_by_css(context, css)) > 0
    assert _retry(check, timeout), u"Element not visible"


def _element_should_not_be_visible(context, css, timeout):
    check = lambda: len(find_visible_by_css(context, css)) == 0
    assert _retry(check, timeout), u"Unexpectedly found visible element(s)"


def _n_elements_should_be_visible(context, expected, css, timeout):
    check = lambda: len(find_visible_by_css(context, css)) == expected
    assert _retry(check, timeout), u"Didn't find exactly {:d} visible elements".format(
        expected
    )


def _at_least_n_elements_should_be_visible(context, expected, css, timeout):
    check = lambda: len(find_visible_by_css(context, css)) >= expected
    assert _retry(check, timeout), u"Didn't find at least {:d} visible elements".format(
        expected
    )


@step(u'the element with the css selector "{css}" should be visible')
def should_see_element_visible_with_css(context, css):
    _element_should_be_visible(context, css, context.browser.wait_time)


@step(
    u'the element with the css selector "{css}" should be visible within {timeout:d} seconds'
)
def should_see_element_visible_with_css_within_timeout(context, css, timeout):
    _element_should_be_visible(context, css, timeout)


@step(u'the element with the css selector "{css}" should not be visible')
def should_not_see_element_visible_with_css(context, css):
    _element_should_not_be_visible(context, css, context.browser.wait_time)


@step(
    u'the element with the css selector "{css}" should not be visible within {timeout:d} seconds'
)
def should_not_see_element_visible_with_css_within_timeout(context, css, timeout):
    _element_should_not_be_visible(context, css, timeout)


@step(u'{n:d} elements with the css selector "{css}" should be visible')
def should_see_n_elements_visible_with_css(context, n, css):
    _n_elements_should_be_visible(context, n, css, context.browser.wait_time)


@step(
    u'{n:d} elements with the css selector "{css}" should be visible within {timeout:d} seconds'
)
def should_see_n_elements_visible_with_css_within_timeout(context, n, css, timeout):
    _n_elements_should_be_visible(context, n, css, timeout)


@step(u'at least {n:d} elements with the css selector "{css}" should be visible')
def should_see_gte_n_elements_visible_with_css(context, n, css):
    _at_least_n_elements_should_be_visible(context, n, css, context.browser.wait_time)


@step(
    u'at least {n:d} elements with the css selector "{css}" should be visible within {timeout:d} seconds'
)
def should_see_gte_n_elements_visible_with_css_within_timeout(context, n, css, timeout):
    _at_least_n_elements_should_be_visible(context, n, css, timeout)
