# logfmt-pandas

This package reads [logfmt](https://www.brandur.org/logfmt) files as [pandas](https://pandas.pydata.org/) DataFrames.

## Usage

```python
from io import StringIO

from logfmt_pandas import read_logfmt

data = StringIO("x=0 y=1\nx=1 y=2")
data_frame = read_logfmt(data)
```

## Testing

Run
```
poetry run pytest
```

## Coverage

Run
```
poetry run pytest --cov
poetry run coverage html
```

Coverage report is written to `htmlcov/index.html`.
