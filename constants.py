#!/usr/bin/env python3

"""
    __name__: constants.py
    __description__: Constants for PDF title, header and index
    __author__: Abdurrahman Ansari
    __version__: 1.0
    __created__: 2020-04-11
    __updated__: 2020-04-19
"""

COL_OUT_CSV_LIST = ("YearMonthDate",
                    "Basic",
                    "House Rent Allowance",
                    "LTA Allowance",
                    "Meal Coupon",
                    "Metrozip Allowance",
                    "Other Fixed Allowance",
                    "Performance Bonus",
                    "Statutory Bonus (Advance)",
                    "Telephone Allowance",
                    "Total",
                    "CalculatedTotal",
                    "Income Tax",
                    "Education Cess",
                    "Provident Fund",
                    "Profession Tax",
                    "LWF",
                    "MealCoupon Deduction",
                    "Deductions",
                    "NetPay")

PDF_NET_PAY_LABEL = "Net Pay : Rs."

COL_PDF_EAR_BASIC = "Basic"
COL_PDF_EAR_HRA = "House Rent Allowance"
COL_PDF_EAR_OFA = "Other Fixed Allowance"
COL_PDF_EAR_MEAL = "Meal Coupon"
COL_PDF_EAR_LTA = "LTA Allowance"
COL_PDF_EAR_TELE = "Telephone Allowance"
COL_PDF_EAR_METRO = "Metrozip Allowance"
COL_PDF_EAR_PERF_BON = "Performance Bonus"
COL_PDF_EAR_STAT_BON = "Statutory Bonus (Advance)"

EARNING_COLS_TUP = (COL_PDF_EAR_BASIC,
                    COL_PDF_EAR_HRA,
                    COL_PDF_EAR_OFA,
                    COL_PDF_EAR_MEAL,
                    COL_PDF_EAR_LTA,
                    COL_PDF_EAR_TELE,
                    COL_PDF_EAR_METRO,
                    COL_PDF_EAR_PERF_BON,
                    COL_PDF_EAR_STAT_BON)

COL_PDF_DED_IT = "Income Tax"
COL_PDF_DED_EC = "Education Cess"
COL_PDF_DED_PF = "Provident Fund"
COL_PDF_DED_PT = "Profession Tax"
COL_PDF_DED_LWF = "LWF"
COL_PDF_DED_MEAL = "MealCoupon Deduction"

DEDUCTION_OLD_COLS_TUP = (COL_PDF_DED_IT,
                          COL_PDF_DED_EC,
                          COL_PDF_DED_PF,
                          COL_PDF_DED_PT,
                          COL_PDF_DED_LWF,
                          COL_PDF_DED_MEAL)

DEDUCTION_NEW_COLS_TUP = (COL_PDF_DED_IT,
                          COL_PDF_DED_EC,
                          COL_PDF_DED_PF,
                          COL_PDF_DED_PT,
                          COL_PDF_DED_MEAL)

DEDUCTION_COLS_TUP = (COL_PDF_DED_IT,
                      COL_PDF_DED_EC,
                      COL_PDF_DED_PF,
                      COL_PDF_DED_PT,
                      COL_PDF_DED_LWF,
                      COL_PDF_DED_MEAL)
