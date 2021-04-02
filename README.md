### Description
The code behind <https://kevingal.com/blog/daylight.html>.

Pulls sunrise / sunset data for different parts of the world in order to make plots like this:

![A graph showing the amount of sunlight in Ireland](https://github.com/Kevinpgalligan/daylight-plots/blob/main/ireland.png)

### Usage
You'll need Python 3.

```
pip3 install -r requirements.txt
```

The script to pull data is `daylight.py`. It has a CLI interface.

```
python3 daylight.py --name ireland
```

The plotting code is in the notebook `plot.ipynb`, and to open it you'll need Jupyter Notebook.
