from pathlib import Path

data_path = Path(__file__).parent

nclist = list((data_path / "data/netcdf").glob("*"))
netcdf = sorted([nc.as_posix() for nc in nclist])
