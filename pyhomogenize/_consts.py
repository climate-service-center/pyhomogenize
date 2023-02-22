frequencies = {
    "1hr": "1H",
    "3hr": "3H",
    "6hr": "6H",
    "6hrPt": "6H",
    "day": "D",
    "week": "7D",
    "mon": ["MS", "M"],
    "monClim": ["MS", "M"],
    "sem": ["QS-DEC", "Q-FEB"],
    "yr": ["AS", "A"],
    "year": ["AS", "A"],
    "fx": None,
}

freqs = {
    "1hr": "1H",
    "3hr": "3H",
    "6hr": "6H",
    "6hrPt": "6H",
    "day": "D",
    "week": "7D",
    "mon": "MS",
    "monClim": "MS",
    "sem": "QS-DEC",
    "yr": "AS",
    "year": "AS",
    "fx": None,
}

translator = {
    "1hr": "hour",
    "3hr": "hour",
    "6hr": "hour",
    "6hrPt": "hour",
    "day": "day",
    "week": "week",
    "mon": "month",
    "monClim": "month",
    "sem": "month",
    "yr": "year",
    "year": "year",
    "fx": None,
}

fmt = {
    "1hr": "%Y-%m-%dT%H:%M",
    "3hr": "%Y-%m-%dT%H:%M",
    "6hr": "%Y-%m-%dT%H:%M",
    "6hrPt": "%Y-%m-%dT%H:%M",
    "day": "%Y-%m-%d",
    "week": "%Y-%m-%d",
    "mon": "%Y-%m",
    "monClim": "%Y-%m",
    "sem": "%Y-%m",
    "yr": "%Y",
    "year": "%Y",
    "fx": None,
}

is_month = {
    "hour": True,
    "day": True,
    "week": True,
    "month": False,
    "sem": False,
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
    "week": [
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
    "sem": [
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
    "year": [
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
    "week": ["year", "month", "day"],
    "mon": ["year", "month"],
    "monClim": ["year", "month"],
    "sem": ["year", "month"],
    "yr": ["year"],
    "year": ["year"],
    "fx": None,
}

naming = {
    "duplicates": "duplicated_timesteps",
    "redundants": "redundant_timesteps",
    "missings": "missing_timesteps",
}

tbounds = {
    "1hr": NotImplemented,
    "3hr": NotImplemented,
    "6hr": NotImplemented,
    "6hrPt": NotImplemented,
    "day": ["D", "D", 12],
    "week": ["7D", "7D", 42],
    "mon": ["MS", "M", 12],
    "monClim": ["MS", "M", 12],
    "sem": ["QS-DEC", "Q-FEB", 12],
    "yr": ["AS", "A", 12],
    "year": ["AS", "A", 12],
    "fx": None,
}
