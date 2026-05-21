from src.visualization.utils import run_query

from src.visualization.chart_utils import (
    create_line_chart,
    create_bar_chart
)

from src.analytics.queries import (
    MONTHLY_REVENUE,
    REVENUE_BY_COUNTRY,
    REVENUE_BY_WEEKDAY
)


def plot_monthly_revenue():

    df = run_query(MONTHLY_REVENUE)

    create_line_chart(
        df=df,
        x_column="Month",
        y_column="MonthlyRevenue",
        title="Monthly Revenue Trend",
        x_label="Month",
        y_label="Revenue"
    )


def plot_revenue_by_country():

    df = run_query(REVENUE_BY_COUNTRY)

    create_bar_chart(
        df=df,
        x_column="Country",
        y_column="TotalRevenue",
        title="Top Revenue Generating Countries",
        x_label="Country",
        y_label="Revenue"
    )


def plot_revenue_by_weekday():

    df = run_query(REVENUE_BY_WEEKDAY)

    create_bar_chart(
        df=df,
        x_column="Weekday",
        y_column="TotalRevenue",
        title="Revenue By Weekday",
        x_label="Weekday",
        y_label="Revenue"
    )


if __name__ == "__main__":

    plot_monthly_revenue()
    plot_revenue_by_country()
    plot_revenue_by_weekday()   