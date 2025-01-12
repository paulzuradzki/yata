function showOrHideEmptyMessage() {
    const itemClass = "todo_item"
    const emptyListId = "todo_items_empty"

    const itemCount = Array.from(document.getElementsByClassName(itemClass)).length;

    if (itemCount === 0) {
        document.getElementById(emptyListId).style.display = "block";
    } else {
        document.getElementById(emptyListId).style.display = "none";
    }
}

window.onload = function() {
    // ID is the target from our form's htmx post
    const targetNode = document.getElementById("todo_items");

    const config = {
        childList: true,
    };

    const observer = new MutationObserver(showOrHideEmptyMessage);
    // watch mutations so the same code will work whether we add or delete items
    observer.observe(targetNode, config);

    // ensure that the correct message is displayed as soon as the page loads
    // else we only call when element is mutated and 
    // show "Nothing to see here..." even with items in DB
    showOrHideEmptyMessage();
};