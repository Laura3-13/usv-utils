# Library

## conda create environment

``` bash
conda create --prefix .venv python=3.10
```

## activate environment

``` bash
conda activate .venv
```

## install library

``` bash
cd # the directory of this file
pip install '-r' requirements.txt
```

## Minimal usage

```python
import barplot

dfs = barplot.read_files("/root", ["name1", "name2"])
```