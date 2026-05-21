from src.visualization.utils import run_query

from src.visualization.chart_utils import (
    create_bar_chart
)

from src.analytics.queries import (
    TOP_CUSTOMERS_BY_REVENUE,
    MOST_FREQUENT_CUSTOMERS,
    CUSTOMER_COUNTRY_DISTRIBUTION
)


def plot_top_customers_by_revenue():

    df = run_query(TOP_CUSTOMERS_BY_REVENUE)

    create_bar_chart(
        df=df,
        x_column="CustomerID",
        y_column="TotalSpent",
        title="Top Customers By Revenue",
        x_label="Customer ID",
        y_label="Revenue",
        figure_size=(12, 6)
    )


def plot_most_frequent_customers():

    df = run_query(MOST_FREQUENT_CUSTOMERS)

    create_bar_chart(
        df=df,
        x_column="CustomerID",
        y_column="TotalOrders",
        title="Most Frequent Customers",
        x_label="Customer ID",
        y_label="Orders",
        figure_size=(12, 6)
    )


def plot_customer_country_distribution():

    df = run_query(CUSTOMER_COUNTRY_DISTRIBUTION)

    create_bar_chart(
        df=df.head(10),
        x_column="Country",
        y_column="TotalCustomers",
        title="Customer Distribution By Country",
        x_label="Country",
        y_label="Customers",
        figure_size=(12, 6)
    )


if __name__ == "__main__":

    plot_top_customers_by_revenue()

    plot_most_frequent_customers()

    plot_customer_country_distribution()