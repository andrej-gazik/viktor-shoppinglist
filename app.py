import streamlit as st
import json
from collections import defaultdict

# Load meal variants
with open("meal_plan_variants.json", "r", encoding="utf-8") as f:
    meals = json.load(f)

# Organize meals by type
meals_by_type = defaultdict(list)
meals_by_id = {}
for meal in meals:
    meals_by_type[meal["type"]].append(meal)
    meals_by_id[meal["id"]] = meal

# Page title
st.title("🥗 4-Day Meal Planner & Shopping List Generator")
st.markdown("Select your meals for the next 4 days. One per category per day.")

# Prepare selection state
days = ["Day 1", "Day 2", "Day 3", "Day 4"]
meal_types = ["Breakfast", "Snack", "Lunch", "Dinner"]

selections = defaultdict(dict)

for day in days:
    st.header(day)
    cols = st.columns(len(meal_types))
    for i, meal_type in enumerate(meal_types):
        with cols[i]:
            options = meals_by_type[meal_type]
            meal_names = [m["name"] for m in options]
            selected = st.selectbox(
                f"{meal_type}",
                meal_names,
                key=f"{day}_{meal_type}"
            )
            selected_id = next((m["id"] for m in options if m["name"] == selected), None)
            selections[day][meal_type] = selected_id

# Generate Shopping List
if st.button("🛒 Generate Shopping List"):
    ingredient_totals = defaultdict(lambda: defaultdict(float))

    for day_meals in selections.values():
        for meal_id in day_meals.values():
            meal = meals_by_id[meal_id]
            for ingredient in meal["ingredients"]:
                item = ingredient["item"].strip().lower()
                amount = ingredient["amount"].strip()
                ingredient_totals[item][amount] += 1  # count frequency of same quantity

    st.subheader("🛍️ Shopping List")
    for item, amounts in ingredient_totals.items():
        for amount, count in amounts.items():
            st.markdown(f"- **{item.title()}**: {amount} × {int(count)}")

    st.success("Shopping list generated based on your selected meals!")
