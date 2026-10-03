from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


# =========================================================
# LOAD DATASET
# =========================================================

df = pd.read_csv("SuperMarket Analysis.csv")

df.columns = df.columns.str.strip()

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")


# =========================================================
# HOME / DASHBOARD
# =========================================================

@app.route("/")
def home():

    # -----------------------------------------------------
    # GET FILTER VALUES
    # -----------------------------------------------------

    selected_branch = request.args.get("branch", "All")
    selected_city = request.args.get("city", "All")
    selected_customer = request.args.get("customer_type", "All")
    selected_gender = request.args.get("gender", "All")
    selected_payment = request.args.get("payment", "All")
    selected_product = request.args.get("product_line", "All")


    # -----------------------------------------------------
    # APPLY FILTERS
    # -----------------------------------------------------

    filtered_df = df.copy()


    if selected_branch != "All":
        filtered_df = filtered_df[
            filtered_df["Branch"] == selected_branch
        ]


    if selected_city != "All":
        filtered_df = filtered_df[
            filtered_df["City"] == selected_city
        ]


    if selected_customer != "All":
        filtered_df = filtered_df[
            filtered_df["Customer type"] == selected_customer
        ]


    if selected_gender != "All":
        filtered_df = filtered_df[
            filtered_df["Gender"] == selected_gender
        ]


    if selected_payment != "All":
        filtered_df = filtered_df[
            filtered_df["Payment"] == selected_payment
        ]


    if selected_product != "All":
        filtered_df = filtered_df[
            filtered_df["Product line"] == selected_product
        ]


    # -----------------------------------------------------
    # DASHBOARD CALCULATIONS
    # -----------------------------------------------------

    total_sales = filtered_df["Sales"].sum()

    total_profit = filtered_df["gross income"].sum()

    total_orders = len(filtered_df)

    total_products = filtered_df["Product line"].nunique()


    # -----------------------------------------------------
    # SALES BY PRODUCT LINE
    # -----------------------------------------------------

    sales_data = (
        filtered_df.groupby("Product line")["Sales"]
        .sum()
        .reset_index()
    )

    product_names = (
        sales_data["Product line"]
        .astype(str)
        .tolist()
    )

    product_sales = (
        sales_data["Sales"]
        .astype(float)
        .tolist()
    )


    # -----------------------------------------------------
    # CATEGORY SALES
    # -----------------------------------------------------

    category_names = product_names

    category_sales = product_sales


    # -----------------------------------------------------
    # SALES BY BRANCH
    # -----------------------------------------------------

    branch_data = (
        filtered_df.groupby("Branch")["Sales"]
        .sum()
        .reset_index()
    )

    branch_names = (
        branch_data["Branch"]
        .astype(str)
        .tolist()
    )

    branch_sales = (
        branch_data["Sales"]
        .astype(float)
        .tolist()
    )


    # -----------------------------------------------------
    # CUSTOMER TYPE
    # -----------------------------------------------------

    customer_data = (
        filtered_df.groupby("Customer type")["Sales"]
        .sum()
        .reset_index()
    )

    customer_names = (
        customer_data["Customer type"]
        .astype(str)
        .tolist()
    )

    customer_sales = (
        customer_data["Sales"]
        .astype(float)
        .tolist()
    )


    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------

    gender_data = (
        filtered_df["Gender"]
        .value_counts()
        .reset_index()
    )

    gender_names = (
        gender_data["Gender"]
        .astype(str)
        .tolist()
    )

    gender_counts = (
        gender_data["count"]
        .astype(int)
        .tolist()
    )


    # -----------------------------------------------------
    # PAYMENT
    # -----------------------------------------------------

    payment_data = (
        filtered_df.groupby("Payment")["Sales"]
        .sum()
        .reset_index()
    )

    payment_names = (
        payment_data["Payment"]
        .astype(str)
        .tolist()
    )

    payment_sales = (
        payment_data["Sales"]
        .astype(float)
        .tolist()
    )


    # -----------------------------------------------------
    # RATING
    # -----------------------------------------------------

    rating_data = (
        filtered_df.groupby("Product line")["Rating"]
        .mean()
        .reset_index()
    )

    rating_names = (
        rating_data["Product line"]
        .astype(str)
        .tolist()
    )

    rating_values = (
        rating_data["Rating"]
        .round(2)
        .astype(float)
        .tolist()
    )


    # -----------------------------------------------------
    # DAILY SALES
    # -----------------------------------------------------

    daily_sales_data = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    daily_dates = (
        daily_sales_data["Date"]
        .dt.strftime("%Y-%m-%d")
        .tolist()
    )

    daily_sales = (
        daily_sales_data["Sales"]
        .astype(float)
        .tolist()
    )


    # -----------------------------------------------------
    # FILTER OPTIONS
    # -----------------------------------------------------

    branches = sorted(df["Branch"].dropna().unique().tolist())

    cities = sorted(df["City"].dropna().unique().tolist())

    customer_types = sorted(
        df["Customer type"].dropna().unique().tolist()
    )

    genders = sorted(
        df["Gender"].dropna().unique().tolist()
    )

    payments = sorted(
        df["Payment"].dropna().unique().tolist()
    )

    product_lines = sorted(
        df["Product line"].dropna().unique().tolist()
    )


    # -----------------------------------------------------
    # SEND DATA TO HTML
    # -----------------------------------------------------

    return render_template(
        "index.html",

        total_sales=float(total_sales),
        total_profit=float(total_profit),
        total_orders=int(total_orders),
        total_products=int(total_products),

        product_names=product_names,
        product_sales=product_sales,

        category_names=category_names,
        category_sales=category_sales,

        branch_names=branch_names,
        branch_sales=branch_sales,

        customer_names=customer_names,
        customer_sales=customer_sales,

        gender_names=gender_names,
        gender_counts=gender_counts,

        payment_names=payment_names,
        payment_sales=payment_sales,

        rating_names=rating_names,
        rating_values=rating_values,

        daily_dates=daily_dates,
        daily_sales=daily_sales,

        # Filter options
        branches=branches,
        cities=cities,
        customer_types=customer_types,
        genders=genders,
        payments=payments,
        product_lines=product_lines,

        # Selected filters
        selected_branch=selected_branch,
        selected_city=selected_city,
        selected_customer=selected_customer,
        selected_gender=selected_gender,
        selected_payment=selected_payment,
        selected_product=selected_product
    )


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)