# Library

## conda create environment

```bash
cd # "the directory of the environment"
```

``` bash
conda create -n neuromatch python=3.10
```

## activate environment

``` bash
conda activate neuromatch
```

## install library

``` bash
pip install '-r' requirements.txt
```

## Minimal usage

```python
import barplot

dfs = barplot.read_files("/root", ["name1", "name2"])
```