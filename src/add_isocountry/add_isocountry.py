import numpy as np
import pandas as pd
import pycountry


def _do_fuzzy_search(country_name: str) -> str:
    try:
        result = pycountry.countries.search_fuzzy(country_name)[0].alpha_3
    except Exception:
        result = np.nan
    return result


def add_isocountry_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Generates country iso codes from column in dataframe

    Returns the new dataframe
    """
    iso_map = {country: _do_fuzzy_search(country) for country in df[col].unique()}
    df["country_code"] = df[col].map(iso_map)
    return df
