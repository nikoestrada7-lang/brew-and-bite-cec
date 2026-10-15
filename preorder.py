"""Member 4: Messenger pre-order form.
Events: submit (validate + confirm), change (live estimate), input (clear errors).
"""
from pyscript import document, when
from products import PRODUCTS, peso

item_select = document.querySelector("#po-item")
qty_input = document.querySelector("#po-qty")
time_select = document.querySelector("#po-time")
estimate = document.querySelector("#po-estimate")
errors = document.querySelector("#po-errors")
confirmation = document.querySelector("#po-confirmation")


def fill_options():
    for p in PRODUCTS:
        opt = document.createElement("option")
        opt.value = p["id"]
        opt.textContent = f"{p['name']} ({peso(p['price'])})"
        item_select.appendChild(opt)
    # Pickup slots every 30 minutes. TODO (group): match your real selling hours.
    for hour in range(9, 17):
        for minute in ("00", "30"):
            suffix = "AM" if hour < 12 else "PM"
            display = hour if hour <= 12 else hour - 12
            opt = document.createElement("option")
            opt.value = f"{display}:{minute} {suffix}"
            opt.textContent = f"{display}:{minute} {suffix}"
            time_select.appendChild(opt)


def find_product(product_id):
    return next(p for p in PRODUCTS if p["id"] == product_id)


def update_estimate():
    try:
        qty = int(qty_input.value)
    except ValueError:
        qty = 0
    qty = max(0, min(qty, 20))
    price = find_product(item_select.value)["price"]
    estimate.textContent = f"Estimated total: {peso(price * qty)}"


@when("change", "#po-item")
def on_item_change(event):
    update_estimate()


@when("input", "#po-qty")
def on_qty_input(event):
    update_estimate()


@when("input", "#preorder-form")   # clear old errors as soon as the user edits anything
def on_any_input(event):
    errors.textContent = ""


@when("submit", "#preorder-form")
def on_submit(event):
    event.preventDefault()  # stop the browser from reloading the page
    name = document.querySelector("#po-name").value.strip()
    messenger = document.querySelector("#po-messenger").value.strip()
    notes = document.querySelector("#po-notes").value.strip()
    problems = []
    if len(name) < 2:
        problems.append("Enter your name (at least 2 characters).")
    if len(messenger) < 2:
        problems.append("Enter your Messenger name so we can confirm your order.")
    try:
        qty = int(qty_input.value)
        if not 1 <= qty <= 20:
            problems.append("Quantity must be between 1 and 20.")
    except ValueError:
        qty = 0
        problems.append("Quantity must be a number.")
    if problems:
        errors.textContent = " ".join(problems)
        confirmation.hidden = True
        return

    product = find_product(item_select.value)
    total = product["price"] * qty
    summary = (f"Hi Brew & Bite CEC! Pre-order for {name}: {qty} × {product['name']}, "
               f"pickup at {time_select.value}. Total {peso(total)}."
               + (f" Notes: {notes}" if notes else ""))
    document.querySelector("#po-summary").textContent = summary
    confirmation.hidden = False
    errors.textContent = ""


fill_options()
update_estimate()
