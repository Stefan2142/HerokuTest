import gspread
import pandas as pd
import datetime as dt


def chunker_list(seq, size):
    """
    Returns a list of lists.
    size - how much sub lists we want
    seq - original list
    Usage tmp = list(chunker_list(l, 10))
    """
    return (seq[i::size] for i in range(size))


def prepare_dataset():

    gc = gspread.service_account(filename="./emailsending-325211-e5456e88f282.json")

    # Nabis Dispatch data
    sh = gc.open_by_url(
        "https://docs.google.com/spreadsheets/d/1rRwdq2otnXI9d3B9LfYRarQl6RxANP0_TqTQLjTY9A8/edit#gid=1032147445"
    )
    wks = sh.worksheet("Sheet6")

    nabis_dispatch_data = pd.DataFrame(
        wks.get_all_records(),
    )

    wks = sh.worksheet("Hours")
    hubstaff_timings_df = pd.DataFrame(wks.get_all_records())
    hubstaff_timings_df["Date"] = pd.to_datetime(
        hubstaff_timings_df["Date"], format="%d/%m/%Y"
    )
    hubstaff_timings_df.rename(columns={"Date": "HS_Date"}, inplace=True)
    nabis_dispatch_data["Total rescheduled"] = nabis_dispatch_data[
        "Total rescheduled"
    ].replace("", 0)
    nabis_dispatch_data = nabis_dispatch_data.fillna(value="")
    nabis_dispatch_data["City"] = nabis_dispatch_data["City"].astype(str)
    nabis_dispatch_data["Your name"] = nabis_dispatch_data["Your name"].astype(str)
    nabis_dispatch_data = nabis_dispatch_data[nabis_dispatch_data["Total orders"] != ""]
    nabis_dispatch_data["Total orders"] = nabis_dispatch_data["Total orders"].astype(
        int
    )
    nabis_dispatch_data["Date"] = pd.to_datetime(
        nabis_dispatch_data.Date, format="%m/%d/%y"
    )
    nabis_dispatch_data["Weekday"] = nabis_dispatch_data["Date"].dt.day_name()
    nabis_dispatch_data.sort_values(by="Date", inplace=True)
    nabis_dispatch_data = pd.merge(
        nabis_dispatch_data,
        hubstaff_timings_df,
        how="left",
        left_on=["Date", "Your name"],
        right_on=["HS_Date", "Member"],
    )
    return nabis_dispatch_data
