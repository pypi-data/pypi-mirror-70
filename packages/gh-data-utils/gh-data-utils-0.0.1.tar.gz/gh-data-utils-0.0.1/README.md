# Greenhouse Data Utilities

The Greenhouse Data Utilities package includes a series of tools to streamline the evaluation of several common experimental designs. It's designed and maintained by the data science team at Greenhouse Software with the intention of installing in a [Mode Analytics](https://app.mode.com/) Python notebook.

Please note that this package was designed for _**internal use**_ by the data science team. You're welcome to use it, but we will prioritize the experimentation needs of our team when reading through issues/feature requests.

## Sub-modules
* gh_data_utils.data_visualization
* gh_data_utils.stat_tests

## `data_visualization`
Functions for generating visual representations of statistical tests.

#### `get_overlapping_distributions`
Generates a Seaborn plot with overlapping distributions between two or more groups in order to visualize potential differences that may be detected with parametric non-parametric statistical tests. These can be used in the final presentation of results.

##### Parameters
- `data`: _pandas dataframe, required_

    Dataframe used to generate charts. Data should be in a [tidy](https://vita.had.co.nz/papers/tidy-data.pdf) format.

- `groups`: _str, required_

  The name of the column in `data` by which you are grouping results.

- `data_col`: _str, required_

  The name of the column in `data` with continuous data to compare by group.

- `order`: _list, optional; default = `None`_

  The order you want groups to appear in the graphs (i.e., Before and After). Must match a list of distinct values in the `groups` parameter.

- `x-label`: _str, optional; default = `''` (empty)_

  x-axis label for the chart.

- `y-label`: _str, optional; default = `''` (empty)_

  y-axis label for the chart.

- `title`: _str, optional; default = `''` (empty)_

  Title for the chart.

- `bins`: _int, required; default = `20`_

  Number of bins for the distributions.

- `tick_format`: _str; options = `'int`, `pct`; default = `'int'`_

  A string indicating the tick format for the graph axes based on the type of data used.

#### `get_barplot`
Generates a Seaborn barplot with error bars in order to visualize mean differences and confidence intervals for those differences between two or more groups. These can be used in the final presentation of results.

##### Parameters
- `data`: _pandas dataframe; required_

    Dataframe used to generate charts. Data should be in a [tidy](https://vita.had.co.nz/papers/tidy-data.pdf) format.

- `groups`: _str; required_

  The name of the column in `data` by which you are grouping results.

- `data_col`: _str; required_

  The name of the column in `data` with continuous data to compare by group.

- `ci`: _int; default = `95`_

  Confidence intervals for the error bars.

- `order`: _list; optional; default = `None`_

  The order you want groups to appear in the graphs (i.e., Before and After). Must match a list of distinct values in the `groups` parameter.

- `hue`: _str; optional; default = `None`_

  Seaborn plot hue in order to generate grouped comparisons.

- `x-label`: _str; default = `''` (empty)_

  x-axis label for the chart.

- `y-label`: _str; default = `''` (empty)_

  y-axis label for the chart.

- `title`: _str; default = `''` (empty)_

  Title for the chart.

- `palette`: _optional; default = `None`_

  Seaborn palette for the chart.

  - `tick_format`: _str; options = `'int`, `pct`; default = `'int'`_

    A string indicating the tick format for the graph axes based on the type of data used.


## `stat_tests`
Functions for conducting the appropriate parametric and non-parametric statistical test based on the specified experimental design and number of groups. We recommend conducting an a priori power analysis to ensure each group you're comparing has a sufficient sample size.

#### `run_stat_test`
Conduct a parametric and non-parametric statistical test for two or more groups. The type of test based on number of groups is determined automatically.

##### Parameters
- `data`: _pandas dataframe; required_

    Dataframe used to generate charts. Data should be in a [tidy](https://vita.had.co.nz/papers/tidy-data.pdf) format.

- `groups`: _str; required_

  The name of the column in `data` by which you are grouping results.

- `data_col`: _str; required_

  The name of the column in `data` with continuous data to compare by group.

- `index`: _str; required_

  The dataframe column to use as an index when shaping data for a specific test. This should be your unit of comparison (i.e., user, day, event, etc).

- `dimensions`: _list; optional; default = `None`_

  A subset of groups to use in statistical comparisons. If this isn't specified, dimensions for statistical tests will be a list of distinct values in `groups`.

- `comparison`: _str; required; options = `'ind`, `rep`; default = `'ind'`_

  The type of experimental design (independent or repeated measures).

- `description`: _str; optional; default = `''`_

  A description of the statistical test to include at the top of the summary of results. Defaults to none, and uses the standard output from each test.
