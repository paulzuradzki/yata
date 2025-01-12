from django.urls import reverse
from playwright.sync_api import Page, expect


def test_create_todo_item_gets_rid_of_nothing_to_see(live_server, page: Page):
    url = reverse_url(live_server, "index")
    page.goto(url)
    page.get_by_label("Title*").fill("Test title")
    page.get_by_label("Description*").fill("Test description")
    page.get_by_role("button", name="Add").click()

    expect(page.get_by_text("Nothing to see here...")).to_be_hidden()


def test_create_todo_item_shows_new_item(live_server, page: Page):
    url = reverse_url(live_server, "index")
    page.goto(url)
    page.get_by_label("Title*").fill("Test title")
    page.get_by_label("Description*").fill("Test description")
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("text=Test title")


def test_display_empty_list_on_first_load(live_server, page: Page):
    url = reverse_url(live_server, "index")
    page.goto(url)
    page.wait_for_selector("text=Nothing to see")


def reverse_url(
    live_server, viewname, urlconf=None, args=None, kwargs=None, current_app=None
):
    end = reverse(viewname, urlconf, args, kwargs, current_app)
    return f"{live_server.url}{end}"
