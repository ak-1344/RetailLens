from src.visualization.utils import run_query

from src.visualization.chart_utils import (
    create_bar_chart
)

from src.analytics.queries import (
    TOP_PRODUCTS_BY_QUANTITY,
    TOP_PRODUCTS_BY_REVENUE,
    MOST_FREQUENTLY_PURCHASED_PRODUCTS
)


def plot_top_products_by_quantity():

    df = run_query(TOP_PRODUCTS_BY_QUANTITY)

    create_bar_chart(
        df=df,
        x_column="Description",
        y_column="TotalQuantitySold",
        title="Top Products By Quantity Sold",
        x_label="Product",
        y_label="Quantity Sold",
        figure_size=(12, 6)
    )


def plot_top_products_by_revenue():

    df = run_query(TOP_PRODUCTS_BY_REVENUE)

    create_bar_chart(
        df=df,
        x_column="Description",
        y_column="TotalRevenue",
        title="Top Products By Revenue",
        x_label="Product",
        y_label="Revenue",
        figure_size=(12, 6)
    )


def plot_most_frequently_purchased_products():

    df = run_query(MOST_FREQUENTLY_PURCHASED_PRODUCTS)

    create_bar_chart(
        df=df,
        x_column="Description",
        y_column="PurchaseFrequency",
        title="Most Frequently Purchased Products",
        x_label="Product",
        y_label="Purchase Frequency",
        figure_size=(12, 6)
    )


if __name__ == "__main__":

    plot_top_products_by_quantity()

    plot_top_products_by_revenue()

    plot_most_frequently_purchased_products()