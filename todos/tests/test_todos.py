from django.urls import reverse
from playwright.sync_api import Page, expect
from todos.models import TodoItem

def test_update_checkbox(live_server, page: Page):
    
    items = [TodoItem.objects.create(title=f"item{i}") for i in range(3)]
    page.goto(reverse(live_server, "index"))
    
    middle_item = items[1]
    middle_id = f"toggle_item_{middle_item.id}"
    page.get_by_test_id(middle_id).to_be_checked()
    expect(page.get_by_test_id(middle_id)).to_be_checked()
    
    middle_item.refresh_from_db()
    assert middle_item.completed is True
    
    items[0].refresh_from_db()
    assert items[0].completed is False
    
    items[2].refresh_from_db()
    assert items[2].completed is False

    # page.get_by_label("Title*").fill("item1")
    # page.get_by_label("Description*").fill("item1 description")
    # page.get_by_role("button", name="Add").click()

    # page.get_by_label("Title*").fill("item2")
    # page.get_by_label("Description*").fill("item2 description")
    # page.get_by_role("button", name="Add").click()

    # page.get_by_label("Title*").fill("item3")
    # page.get_by_label("Description*").fill("item3 description")
    # page.get_by_role("button", name="Add").click()

    # page.get_by_label("Title*").fill("item4")
    # page.get_by_label("Description*").fill("item4 description")
    # page.get_by_role("button", name="Add").click()

    # page.get_by_test_id("toggle_item_1").check()
    # page.get_by_test_id("toggle_item_2").check()
    # page.get_by_test_id("toggle_item_3").check()
    # page.get_by_test_id("toggle_item_4").check()

def test_display_one_item_on_first_load(live_server, page: Page):
    TodoItem.objects.create(title="Test item")
    page.goto(reverse_url(live_server, "index"))
    page.wait_for_selector("text=Test item")  # select DOM elements
    expect(page.get_by_text("Nothing to see here..")).to_be_hidden()


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
