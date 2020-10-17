#!/usr/bin/env python3

"""
Copyright 2020 Abdurrahman Ansari

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
    __name__: pay_slip_analysis.py
    __description__: Process & parse PaySlips & merge them into a CSV and create visualization
    __author__: Abdurrahman Ansari
    __version__: 1.0
    __created__: 2020-03-15
    __updated__: 2020-04-19
"""

import os
import datetime
from dateutil import parser
import calendar
import locale
import logging

import functools

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import tabula

from constants import COL_OUT_CSV_LIST
from constants import EARNING_COLS_TUP
from constants import DEDUCTION_COLS_TUP
from constants import DEDUCTION_OLD_COLS_TUP
from constants import DEDUCTION_NEW_COLS_TUP
from constants import PDF_NET_PAY_LABEL

from environment import Env

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

DF_COLUMN_DICT = {
    "value_index": 2,
    "net_pay_index": 4,
    "df_year_month_index": 0,
    "earning_title_column": None,
    "earning_current_column": "Unnamed: 1",
    "earning_all_column": "Unnamed: 2",
    "deduction_title_column": "Unnamed: 3",
    "deduction_current_column": "Unnamed: 4",
    "deduction_all_column": "Unnamed: 5",
    "net_pay_column": None
}


def main():
    """
    1. Read and parse PDF files into month-wise DF
    2. Create CSV by combining all the DFs
    3. Create visualizations from the CSV
    :return: None
    """

    logger = Env.setup_logging()

    path_base = os.path.join(os.getcwd(), "PDF")
    csv_path = os.path.join(os.getcwd(), "output", "Salary_Slips_Merged.csv")

    pdf_path_list = sorted([os.path.join(path_base, file_name) for file_name in os.listdir(path_base) if
                            (os.path.isfile(os.path.join(path_base, file_name)) and
                             os.path.basename(file_name).endswith(".pdf") and ("Pay" in file_name))])

    combined_payslip_df = pd.DataFrame()

    for pdf_path in pdf_path_list:
        monthly_df = pdf_to_df(pdf_path, logger)
        combined_payslip_df = combined_payslip_df.append(monthly_df)

    combined_payslip_df.to_csv(csv_path, index=None)

    if not os.path.exists(os.path.dirname(csv_path)):
        os.mkdir(os.path.dirname(csv_path))

    side_by_side_bar_plot(csv_path)

    line_plot(csv_path)


def side_by_side_bar_plot(csv_path):
    """
    Create month wise side by side bar plot of deduction, net pay and total salary and persist the same
    :param csv_path: Absolute CSV path of the combined payslips
    :return: None
    """
    csv_df = pd.read_csv(csv_path)

    csv_df["YearMonth"] = csv_df["YearMonthDate"].apply(
        lambda ymd: str(datetime.datetime.strftime(parser.parse(ymd), "%b-%y")))

    # Get desired columns
    df = csv_df[["YearMonth", "Deductions", "NetPay", "Total"]]

    # Massage DF into
    melt_df = df.melt(id_vars='YearMonth').rename(columns=str.title)

    # Create color palette
    rgb_palette = ["#e74c3c", "#2ecc71", "#3498db"]

    # Create subplots
    sns.set()
    fig, ax = plt.subplots(figsize=(15, 10))

    # Create bar plot
    graph = sns.barplot(x='Yearmonth', y='Value', hue='Variable', data=melt_df, ax=ax, palette=rgb_palette)

    # Enhance graph, label, font and alignment
    beautify_graph(graph, ax)

    sns.despine(fig)

    plt.savefig(os.path.join(os.getcwd(), "output", "side_by_side_bar_graph.png"))

    plt.show()


def line_plot(csv_path):
    """
    Create month wise trend line graph of deduction, net pay and total salary and persist the same
    :param csv_path: Absolute CSV path of the combined payslips
    :return: None
    """
    csv_df = pd.read_csv(csv_path)

    df = csv_df[["YearMonthDate", "Deductions", "NetPay", "Total"]]
    tidy = df.melt(id_vars='YearMonthDate').rename(columns=str.title)

    sns.set()
    fig, ax = plt.subplots(figsize=(15, 10))
    # Create color palette
    rgb_palette = ["#e74c3c", "#2ecc71", "#3498db"]

    graph = sns.lineplot(x='Yearmonthdate', y='Value', hue='Variable', data=tidy, palette=rgb_palette)

    for item in graph.get_xticklabels():
        item.set_rotation(90)

    beautify_graph(graph, ax)

    sns.despine(fig)
    plt.savefig(os.path.join(os.getcwd(), "output", "trend_line_graph.png"))
    plt.show()


def beautify_graph(graph, ax):
    """
    Set ticks, labels and fonts
    :param graph: Graph object
    :param ax: Axis object
    :return: None
    """

    # Set label padding
    ax.xaxis.labelpad = 15
    ax.yaxis.labelpad = 15

    # Change tick font size
    ax.xaxis.set_tick_params(labelsize=10)
    ax.yaxis.set_tick_params(labelsize=10)

    # Change tick padding
    ax.tick_params(axis='x', which='major', pad=3)
    ax.tick_params(axis='y', which='major', pad=3)

    # Change rotation of X tick labels
    for item in graph.get_xticklabels():
        item.set_rotation(90)

    # Get rid of title in legend
    leg = graph.axes.get_legend()
    leg.set_title(None)

    # Set thousand separator for y axis
    ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    # Set labels and title
    ax.set_ylabel('Amount (₹)')
    ax.set_xlabel('Year Month')
    ax.set_title('Monthly Salary Analysis')


def pdf_to_df(pdf_path: str, logger: logging.Logger) -> pd.DataFrame:
    """
    Read PDF into unorganized DF using tabula; extract and organize the columns and values into a DF
    :param pdf_path: Absolute path of the salary PDF
    :param logger: Logger object
    :return: DF of monthly salary details
    """

    # Don't output warnings if there are any
    pdf_df = tabula.read_pdf(pdf_path, silent=True)

    column_month_name = pdf_df.columns[0]
    year_month_date = get_year_month(pdf_df)
    logger.info(f"{year_month_date}")
    DF_COLUMN_DICT["earning_title_column"] = column_month_name
    DF_COLUMN_DICT["net_pay_column"] = column_month_name

    emp_title = pdf_df[column_month_name].iloc[0].splitlines()
    emp_value = pdf_df["Unnamed: 1"].iloc[0].splitlines()

    """
        Earning Current Month
    """
    earning_current_title = pdf_df[column_month_name].iloc[2].splitlines()
    earning_current_value = pdf_df["Unnamed: 1"].iloc[2].splitlines()
    earning_current_list = to_float_list(earning_current_value)
    earning_to_date_value = pdf_df["Unnamed: 2"].iloc[2].splitlines()

    """
        Deduction Current Month
    """
    deduction_title = pdf_df["Unnamed: 3"].iloc[2].splitlines()
    deduction_current_value = pdf_df["Unnamed: 4"].iloc[2].splitlines()
    deduction_current_list = to_float_list(deduction_current_value)
    deduction_to_date_value = pdf_df["Unnamed: 5"].iloc[2].splitlines()
    check_ded_col = validate_deduction_cols(year_month_date, deduction_title)
    if not check_ded_col:
        logger.critical(f"Deduction column check failed")
    deduction_current_dict = dict(zip(deduction_title, deduction_current_list))

    net_pay_lines = pdf_df[DF_COLUMN_DICT["net_pay_column"]].iloc[DF_COLUMN_DICT["net_pay_index"]].splitlines()
    net_pay_amount = locale.atof(str(net_pay_lines[0]).replace(PDF_NET_PAY_LABEL, ""))

    current_total = functools.reduce(lambda x, y: x + y, earning_current_list)
    current_deduction = functools.reduce(lambda x, y: x + y, deduction_current_list)

    earning_current_dict = dict(zip(earning_current_title, earning_current_list))
    earning_current_dict["YearMonthDate"] = year_month_date
    earning_current_dict["CalculatedTotal"] = current_total

    earning_deduction_dict_list = [{**earning_current_dict, **deduction_current_dict}]
    earning_current_df = pd.DataFrame(earning_deduction_dict_list)
    earning_current_df.set_index("YearMonthDate")

    for column in EARNING_COLS_TUP:
        if column not in earning_current_df.columns:
            earning_current_df[column] = 0.0

    for column in DEDUCTION_COLS_TUP:
        if column not in earning_current_df.columns:
            earning_current_df[column] = 0.0

    earning_current_df["Total"] = earning_current_df[list(EARNING_COLS_TUP)].sum(axis=1)
    earning_current_df["Deductions"] = earning_current_df[list(DEDUCTION_COLS_TUP)].sum(axis=1)
    earning_current_df["NetPay"] = net_pay_amount

    earning_current_df = earning_current_df.reindex(columns=COL_OUT_CSV_LIST)

    earning_to_date_list = [dict(zip(earning_current_title, earning_to_date_value))]
    earning_to_date_df = pd.DataFrame(earning_to_date_list)

    return earning_current_df


def validate_deduction_cols(year_month_date: datetime.datetime, deduction_cols: list) -> bool:
    """
    Check if all the deduction columns are present or not
    :param year_month_date: Date time object
    :param deduction_cols: Deduction columns to check
    :return: True if all the columns present else false
    """
    last_lwf_date = datetime.datetime(2019, 3, 31)

    deduction_gt_cols = DEDUCTION_NEW_COLS_TUP if year_month_date > last_lwf_date else DEDUCTION_OLD_COLS_TUP

    return all(x in deduction_cols for x in deduction_gt_cols)


def to_float_list(str_list):
    return list(map(lambda x: locale.atof(x), str_list))


def get_year_month(df):
    """
    Convert payslip specific date format to standardized one
    :param df: DF representing monthly payslip
    :return: datetime of that month
    """
    column_month_name = df.columns[0]
    column_part_list = column_month_name.split()
    year_month_str = column_part_list[3] + " " + column_part_list[4]
    year_month_date = datetime.datetime.strptime(year_month_str, "%B %Y")

    return year_month_date


def first_last_dates_of_month(current_year, current_month):
    """
    Get first and last date of the year and month
    :param current_year:
    :param current_month:
    :return: Tuple of first and last dates
    """

    _, num_days = calendar.monthrange(current_year, current_month)
    first_day = datetime.datetime(current_year, current_month, 1)
    last_day = datetime.datetime(current_year, current_month, num_days)

    return first_day, last_day


def current_month_first_last_dates():
    """
    Get first and last date of the current year and month
    :return: Tuple of first and last dates
    """
    now = datetime.datetime.now()

    year = now.year
    month = now.month

    return first_last_dates_of_month(year, month)


if __name__ == '__main__':
    main()
