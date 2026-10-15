"""Member 2: menu page. Event: click on category filter buttons."""
from pyscript import document, when
from products import PRODUCTS, peso

grid = document.querySelector("#menu-grid")
count = document.querySelector("#menu-count")


def render(category="All"):
    """Redraw the menu cards for the chosen category."""
    items = [p for p in PRODUCTS if category == "All" or p["category"] == category]
    grid.innerHTML = ""
    for p in items:
        card = document.createElement("article")
        card.className = "menu-item"
        card.innerHTML = (
            f"<h3>{p['name']}</h3><p>{p['desc']}</p>"
            f"<span class='price'>{peso(p['price'])}</span>"
        )
        grid.appendChild(card)
    count.textContent = f"Showing {len(items)} item(s)"


@when("click", ".filter-btn")
def on_filter_click(event):
    clicked = event.currentTarget
    for btn in document.querySelectorAll(".filter-btn"):
        btn.classList.remove("active")
        btn.setAttribute("aria-pressed", "false")
    clicked.classList.add("active")
    clicked.setAttribute("aria-pressed", "true")
    render(clicked.getAttribute("data-category"))


render()
