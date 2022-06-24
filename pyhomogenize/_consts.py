frequencies = {
    "1hr": "1H",
    "3hr": "3H",
    "6hr": "6H",
    "6hrPt": "6H",
    "day": "D",
    "mon": ["MS", "M"],
    "monClim": ["MS", "M"],
    "yr": ["AS", "A"],
    "fx": None,
}

translator = {
    "1hr": "hour",
    "3hr": "hour",
    "6hr": "hour",
    "6hrPt": "hour",
    "day": "day",
    "mon": "month",
    "monClim": "month",
    "yr": "year",
    "fx": None,
}

format = {
    "1hr": "%Y-%m-%dT%H:%M",
    "3hr": "%Y-%m-%dT%H:%M",
    "6hr": "%Y-%m-%dT%H:%M",
    "6hrPt": "%Y-%m-%dT%H:%M",
    "day": "%Y-%m-%d",
    "mon": "%Y-%m",
    "monClim": "%Y-%m",
    "yr": "%Y",
    "fx": None,
}

is_month = {
    "hour": True,
    "day": True,
    "month": False,
    "year": False,
    None: False,
}

equalize = {
    "1hr": [
        "second",
        "microsecond",
        "nanosecond",
    ],
    "3hr": [
        "second",
        "microsecond",
        "nanosecond",
    ],
    "6hr": [
        "second",
        "microsecond",
        "nanosecond",
    ],
    "6hrPt": [
        "second",
        "microsecond",
        "nanosecond",
    ],
    "day": [
        "hour",
        "minute",
        "second",
        "microsecond",
        "nanosecond",
    ],
    "mon": [
        "day",
        "hour",
        "minute",
        "second",
        "microsecond",
        "nanosecond",
    ],
    "monClim": [
        "day",
        "hour",
        "minute",
        "second",
        "microsecond",
        "nanosecond",
    ],
    "yr": [
        "month",
        "day",
        "hour",
        "minute",
        "second",
        "microsecond",
        "nanosecond",
    ],
}

within = {
    "1hr": NotImplemented,
    "3hr": NotImplemented,
    "6hr": NotImplemented,
    "6hrPt": NotImplemented,
    "day": ["year", "month", "day"],
    "mon": ["year", "month"],
    "monClim": ["year", "month"],
    "yr": ["year"],
    "fx": None,
}

naming = {
    "duplicates": "duplicated_timesteps",
    "redundants": "redundant_timesteps",
    "missings": "missing_timesteps",
}
