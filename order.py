"""Member 3: order calculator.
Events: input (live total), change (discount checkbox), click (place / clear order).
"""
from pyscript import document, when
from products import PRODUCTS, STUDENT_DISCOUNT, peso

order_list = document.querySelector("#order-list")
subtotal_el = document.querySelector("#subtotal")
discount_el = document.querySelector("#discount")
total_el = document.querySelector("#total")
receipt = document.querySelector("#receipt")
message = document.querySelector("#order-message")


def build_rows():
    for p in PRODUCTS:
        row = document.createElement("div")
        row.className = "order-row"
        row.innerHTML = (
            f'<label for="qty-{p["id"]}"><span class="name">{p["name"]}</span>'
            f'<span class="price">{peso(p["price"])}</span></label>'
            f'<input type="number" id="qty-{p["id"]}" class="qty" '
            f'min="0" max="20" value="0" inputmode="numeric">'
        )
        order_list.appendChild(row)


def get_quantities():
    """Read each quantity box, treating blanks and bad values as 0 (max 20)."""
    quantities = {}
    for p in PRODUCTS:
        raw = document.querySelector(f"#qty-{p['id']}").value
        try:
            n = int(raw)
        except ValueError:
            n = 0
        quantities[p["id"]] = max(0, min(n, 20))
    return quantities


def compute():
    """Return (lines, subtotal, discount, total)."""
    quantities = get_quantities()
    lines = [(p["name"], quantities[p["id"]], p["price"] * quantities[p["id"]])
             for p in PRODUCTS if quantities[p["id"]] > 0]
    subtotal = sum(line[2] for line in lines)
    is_student = document.querySelector("#student").checked
    discount = subtotal * STUDENT_DISCOUNT if is_student else 0
    return lines, subtotal, discount, subtotal - discount


def refresh():
    _, subtotal, discount, total = compute()
    subtotal_el.textContent = peso(subtotal)
    discount_el.textContent = f"-{peso(discount)}"
    total_el.textContent = peso(total)


@when("input", "#order-list")      # fires on every keystroke / arrow click in a quantity box
def on_quantity_input(event):
    refresh()


@when("change", "#student")        # fires when the discount checkbox is toggled
def on_discount_toggle(event):
    refresh()


@when("click", "#place-order")
def on_place_order(event):
    name = document.querySelector("#customer-name").value.strip()
    lines, subtotal, discount, total = compute()
    if not lines:
        message.textContent = "Add at least one item before placing your order."
        message.className = "msg error"
        return
    if not name:
        message.textContent = "Enter your name so we know who the order is for."
        message.className = "msg error"
        return
    message.textContent = ""
    message.className = "msg"
    rows = "".join(f"<li>{qty} × {item}: {peso(amt)}</li>" for item, qty, amt in lines)
    receipt.innerHTML = f"<h3>Order summary</h3><ul>{rows}</ul><p class='receipt-total'>Total: {peso(total)}</p>"
    # Use textContent for user-typed text so it can never inject HTML
    who = document.createElement("p")
    who.textContent = f"Thanks, {name}! Your order is ready to confirm through Messenger."
    receipt.insertBefore(who, receipt.firstChild)
    receipt.hidden = False


@when("click", "#clear-order")
def on_clear(event):
    for field in document.querySelectorAll(".qty"):
        field.value = "0"
    document.querySelector("#customer-name").value = ""
    document.querySelector("#student").checked = False
    receipt.hidden = True
    message.textContent = ""
    refresh()


build_rows()
refresh()
