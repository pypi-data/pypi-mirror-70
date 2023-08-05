# Hyperparameter Optimization on the Grid
This package provides a framework for performing hyperparameter optimization (HPO) using the ATLAS grid resources. 

# Table of Contents
1.  [Basic Workflow](#basic-workflow)
2.  [Getting the code](#getting-the-code)
3.  [Setup and Installation](#setup-and-installation)
    * [Using the default conda environment](#using-the-default-conda-environment)
    * [Inside a custom virtual environment](#inside-a-custom-virtual-environment)
4.  [How to](#how-to)
5.  [Adapting training scripts for hyperparameter optimization](#adapting-training-scripts-for-hyperparameter-optimization)
6.  [Managing Configuration Files](#managing-configuration-files)
    * [HPO Configuration](#hpo-configuration)
    * [Grid Configuration](#grid-configuration)
    * [Model Configuration](#model-configuration)
    * [Search Space onfiguration](#search-space-configuration)
7.  [Running Hyperparameter Optimization Jobs](#Running-Hyperparameter-Optimization-Jobs)
8.  [Monitoring Job Status](#monitoring-job-status)
9.  [Visualizing Hyperparamter Optimization Results](#visualizing-hyperparameter-optimization-results)
10.  [Command line options](#command-line-options)
11. [Important Notes](#important-notes)
    * [Working Directory of Container](#working-directory-of-contaianer)
    * [Location of Input Dataset](#location-of-input-datatset)
    * [Digest of Grid Site Errors](#digest-of-grid-site-errors)

# Basic Workflow

<img src="https://gitlab.cern.ch/clcheng/ReadmeImagery/-/raw/master/images/hpogrid/WorkflowDiagram.png" width="800">

The execution of the above hyperparameter optimization workflow can be done entirely using the _hpogrid tool_ provided by this repository. The sample usage and instruction for using the _hpogrid tool_ is given in the next few sections.

The workflow can be divided into the following steps:

**Step 1**: Prepare the configuration files for a hyperparameter optimization task which will submitted to the ATLAS grid site. A total of four configuration files are required. They are:
1. **HPO Configuration**: Configurations that define how the hyperparameter optimization is performed. This may include the algorithm of hyperparameter optimization, the scheduling method for choosing the next hyperparameter points, the number of hyperparameter points to be evaluated and so on.
2. **Search Space Configuration**: Configurations that define the hyperparameter search space. This includes the sampling method for a particular hyperparameter (such as uniform or normal sampling or logirthmic based uniform sampling) and its range of allowed values.
3. **Model Configuration**: Configurations that contains information of the training model that is called by the hyperparameter optimization alogrithm. This should include 
    * The name of the training script which contains the class/function defining the training model
    * The name of the class/function that defines the training model
    * The parameters that should be passed to the training model. For details please refer to the section (Adaptation of Training Script)
4. **Grid Configuration**: Configurations that define settings for grid job submission. This may include the container inside which the scripts are run, the name of input and output datasets and the name of the grid site where the hyperparameter optimization jobs are run. 

**Step 2**: Upload the input dataset via rucio which will be retrieved by the grid site when the hyperparameter optimization task is executed.

**Step 3**: Adapt the training script(s) to conform with the format required by the hyperparameter optimization library (Ray Tune).

**Step 4**: Submit the hyperparamter optimization task and monitor its progress.

**Step 5**: Retrieve the hyperparamter optimization results after completion. The results can be output into various formats supported by the _hpogrid tool_ for visualization. 

# Getting the code
To get the code, use the following command:
```
git clone ssh://git@gitlab.cern.ch:7999/aml/hyperparameter-optimization/alkaid-qt/hpogrid/hpogrid.git
```

# Setup and Installation

### Using the default conda environment

To setup just use the command (from the base path of the project):
```
source setupenv.sh
```
This will setup the default conda environment _ml-base_ which contains all necessary machine-learning packages and the latest version of ROOT.

### Inside a custom virtual environment

Activate your custom environment then use the command (from the base path of the project):
```
source setupenv.sh no-conda
```
Then install the hpogrid package:
```
pip install hpogrid

```

# How to

* For details of how to **adapt a training script to the HPO library**, please refer to [this section](#adapting-training-scripts-for-hyperparameter-optimization)
* For details of how to **create, update, display a configuration file**, please refer to [this section](#managing-configuration-files)

### Example 1: Optimizing a simple objective function

Given a simple objective function `loss = (height - 14)**2 - abs(width - 3)`  with `-100 < height < 100` and `0 < width < 20`. The goal is to minimize the metric `loss`.
The training script with the above objective function can be found in `example/scripts/simple_objective.py`. 

```
# Create Configuration Files
hpogrid model_config create simple_objective_model --script simple_objective.py --model simple_objective
hpogrid search_space create simple_objective_space '{"height":{"method":"uniform","dimension":{"low":-100,"high":100}}, "width":{"method":"uniform","dimension":{"low":0,"high":20}}}'
hpogrid hpo_config create random_search_min_loss --algorithm random --metric loss --mode min --trials 200
hpogrid grid_config create manc_standard --site ANALY_MANC_GPU_TEST
# Create a Project with the Configuration Files
hpogrid project create simple_objective --scripts_path ${HPOGRID_BASE_PATH}/example/scripts/simple_objective.py --model_config simple_objective_model --search_space simple_objective_space --hpo_config random_search_min_loss --grid_config manc_standard
# Submit Grid Jobs corresponding to the Project
hpogrid run simple_objective --n_jobs 3
```
### Example 2: Optimizing a simple trainable class

The training script with the above trainable class can be found in `example/scripts/simple_trainable.py`


```
# Create Configuration Files
hpogrid model_config create simple_trainable_model --script simple_trainable.py --model MyTrainableClass
hpogrid search_space create simple_trainable_space '{"alpha":{"method":"uniform","dimension":{"low":-10,"high":10}}, "beta": {"method":"categorical","dimension":{"categories":[-1,0,1,2,3,4,5]}}}'
hpogrid hpo_config create bayesian_min_loss --algorithm bayesian --metric loss --mode min --trials 200
# If you have already created the grid config manc_standard, you may skip the following line
hpogrid grid_config create manc_standard --site ANALY_MANC_GPU_TEST
# Create a Project with the Configuration Files
hpogrid project create simple_trainable --scripts_path ${HPOGRID_BASE_PATH}/example/scripts/simple_trainable.py --model_config simple_trainable_model --search_space simple_trainable_space --hpo_config bayesian_min_loss --grid_config manc_standard
# Submit Grid Jobs corresponding to the Project
hpogrid run simple_trainable --n_jobs 3
```

### Example 3: Optimizing a convolutional neural network for the MNIST dataset

```
# Create Configuration Files
hpogrid model_config create mnist_cnn --script mnist.py --model MNISTTrainable
hpogrid search_space create mnist_cnn_space '{"hidden": {"method": "categorical", "dimension": {"categories": [32, 64, 128]}},"batchsize": {"method": "categorical", "dimension": {"categories": [32, 64, 128, 256, 512]}}, "lr": {"method": "loguniform", "dimension": {"low": 4.5e-05, "high": 1.83e-2}}, "beta": {"method": "uniform", "dimension": {"low": 0.5, "high": 1.0}}}'
hpogrid hpo_config create hyperopt_min_loss --algorithm hyperopt --mode min --trials 200
# If you have already created the grid config manc_standard, you may skip the following line
hpogrid grid_config create manc_standard --site ANALY_MANC_GPU_TEST
# Create a Project with the Configuration Files
hpogrid project create mnist_cnn --scripts_path ${HPOGRID_BASE_PATH}/example/scripts/mnist.py --model_config mnist_cnn --search_space mnist_cnn_space --hpo_config hyperopt_min_loss --grid_config manc_standard
# Submit Grid Jobs corresponding to the Project
hpogrid run simple_trainable --n_jobs 3
```

# Adapting training scripts for hyperparameter optimization

# Managing Configuration Files

In general, the command for managing configuraton file takes the form:
```
hpogrid <config_type> <action> <config_name> [<options>]
```

The `<config_type>` argument specifies the type of configuration to be handled. The avaliable types are
- `hpo_config` : Configuration for hyperparamter optimization
- `grid_config` : Configuration for grid job submission
- `model_config` : Configuration for the machine learning model (which the hyperparameters are to be optimized)
- `search_space` : Configuration for the hyperparameter search space

The `<action>` argument specifies the action to be performed. The available actions are
- `create` : Create a new configuration
- `recreate` : Recreate an existing configuration (the old configuration will be overwritten)
- `update` : Update an existing configuration (the old configuration except those to be updated will be kept)
- `remove` : Remove an existing configuration
- `list` : List the name of existing configurations (the `<config_name>` argument is omitted)
- `show` : Display the content of an existing configuration

The `<config_name>` argument specifies name given to a configuration file. 

The `[<options>]` arguments specify the configuration settings for the corresponding configuration type. The available options are explained below.

## HPO Configuration

 
| **Option** | **Description** | **Default** | **Choices** |
| ---------- | ---------- | ----------- | ----------- |
| `algortihm` | Algorithm for hyperparameter optimization | 'random' | 'hyperopt', 'skopt', 'bohb', 'ax', 'tune', 'random', 'bayesian' |
| `metric` | Evaluation metric to be optimized | 'accuracy' | - |
| `mode` | Optimization mode (either 'min' or 'max')| 'max' | 'max', 'min'
| `scheduler` | Trial scheduling method for hyperparameter optimization | 'asynchyperband' | 'asynchyperband', 'bohbhyperband', 'pbt' |
| `trials` | Number of trials (search points) | 100 | - |
| `log_dir` | Logging directory | "./log" | - |
| `verbose` | Check to enable verbosity | - | - |
| `stop` | Stopping criteria | '{"training_iteration": 1}' | - |
| `scheduler_param` | extra parameters for the trial scheduler | '{"max_concurrent": 4}' | - |
| `algorithm_param` | extra parameters for hyperparameter optimization algorithm | {} | - |


## Grid Configuration


| **Option** | **Description** | **Default** | 
| ---------- | ---------- | ----------- | 
| `site` | Grid site where the jobs are submitted | ANALY_MANC_GPU_TEST | 
| `container` | Docker or singularity container which the jobs are run | /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/aml/hyperparameter-optimization/alkaid-qt/hpogrid:latest | 
| `retry` | Check to enable retrying faild jobs | - | 
| `inDS` | Name of input dataset | - | 
| `outDS` | Name of output dataset | user.${{RUCIO_ACCOUNT}}.hpogrid.{HPO_PROJECT_NAME}.out.$(date +%Y%m%d%H%M%S) |


## Model Configuration

This defines the parameters and settings for the machine learning model which the hyperparameters are to be optimized.


| **Option** | **Description** |
| ---------- | ---------- | 
| `script` | Name of the training script where the function or class that defines the training model will be called to perform the training|
| `model` | Name of the function or class that defines the training model |
| `param` | Extra parameters to be passed to the training model |




## Search Space Configuration

This defines the search space for hyperparameter optimization.

The format for defining a search space in command line is through a json decodable string:
```
'{"NAME_OF_HYPERPARAMETER":{"method":"SAMPLING_METHOD","dimension":{"DIMENSION":"VALUE"}},
"NAME_OF_HYPERPARAMETER":{"method":"SAMPLING_METHOD","dimension":{"DIMENSION":"VALUE"}}, ...}'
```

Supported sampling methods for a hyperparameter:

| **Method** | **Description** | **Dimension**  |
| ---------- | --------------- | -------------- | 
| `categorical` | Returns one of the values in `categories`, which should be a list. If `grid_search`is set to 1, each value must be sampled once.| `categories`, `grid_search`| 
| `uniform`  | Returns a value uniformly between `low` and `high` | `low`, `high` |
| `uniformint` | Returns an integer value uniformly between `low` and `high` |  `low`, `high` | 
| `quniform` | Returns a value like round(uniform(`low`, `high`) / `q`) * `q` | `low`, `high`, `q` | 
| `loguniform` | Returns a value drawn according to exp(uniform(`low`, `high`)) so that the logarithm of the return value is uniformly distributed. | `low`, `high`, `base` |
| `qloguniform` | Returns a value like round(exp(uniform(`low`, `high`)) / `q`) * `q`|  `low`, `high`, `base`, `q` |
| `normal` | Returns a real value that's normally-distributed with mean `mu` and standard deviation `sigma`.| `mu`, `sigma` |
| `qnormal` | Returns a value like round(normal(`mu`, `sigma`) / `q`) * `q`| `mu`, `sigma`, `q`| 
| `lognormal` | Returns a value drawn according to exp(normal(`mu`, `sigma`)) so that the logarithm of the return value is normally distributed.| `mu`, `sigma`, `base`|
| `qlognormal` |  Returns a value like round(exp(normal(`mu`, `sigma`)) / `q`) * `q`| `mu`, `sigma`, `base`, `q`|

Examples:
```
hpogrid search_space create my_search_space '{ "lr":{"method":"loguniform","dimension":{"low":1e-5,"high":1e-2, "base":10}},\
"batchsize":{"method":"categorical","dimension":{"categories":[32,64,128,256,512,1024]}},\
"num_layers":{"method":"uniformint","dimension":{"low":3,"high":10}},\
"momentum":{"method":"uniform","dimension":{"low":0.5,"high":1.0}} }'
```



# Running Hyperparameter Optimization Jobs

**Step 1**: Create a custom project with the configuration files:
 ```
 hpogrid project create <project_name> [--options]
 ```
 
| **Option** | **Description** |
| ---------- | --------------- |
| `scripts_path` | the path to where the training scripts (or the directory containing the training scripts) are located |
| `hpo_config` | the hpo configuration to use for this project |
| `grid_config` | the grid configuration to use for this project |
| `model_config` | the model configuration to use for this project |
| `search_space` | the search space configuration to use for this project |


**Step 2**: Run the project:

- To run locally:

```
hpogrid local_run PROJECT_NAME
```

- To run on the grid:

```
hpogrid run <project_name> [--options]
```

| **Option** | **Description** |  **Default** |
| ---------- | ---------- | ------------ |
| `n_jobs` | the number of grid jobs to be submitted (useful for random search, i.e. to run a single search point per job) | 1 |
| `site` | the site to where the jobs are submitted (this will override the site setting in the grid configuration | - |


# Monitoring Job Status

To get the status of recent grid jobs:

```
hpogrid tasks show [--options]
```

| **Option** | **Description** |  **Default** |
| ---------- | ---------- | ------------ |
| `username` | filter tasks by username | 1 |
| `limit` | the maximum number of tasks to query | 1000 |
| `days` | filter tasks within the recent `N` days | 30 |
| `taskname` | filter tasks by taskname (accept wildcards) | - |
| `jeditaskid` | only show the task with the specified jeditaskid | - |
| `metadata` | print out the metadata of a task | False |
| `sync` | force no caching on the PanDA server | False |
| `range` | filter tasks by jeditaskid range | - |
| `output` | output result with the filename if specified | - |
| `outcol` | data columns to be saved in output | 'jeditaskid', 'status', 'taskname', 'computingsite', 'metastruct' | 



# Visualizing Hyperparamter Optimization Results
To get the hpo result for a specific project:
```
hpogrid report <project_name> [--options]
```
| **Option** | **Description** |  **Default** | **Choices** | 
| ---------- | --------------- | ------------ | ----------- |
| `limit` | the maximum number of tasks to query | 1000 | - |
| `days` | filter tasks within the recent `N` days | 30 | - |
| `taskname` | filter tasks by taskname (accept wildcards) | - | - |
| `range` | filter tasks by jeditaskid range | - | - |
| `extra` | extra data columns to be displayed and saved | - | 'site', 'task_time_s', 'time_s', 'taskid' |
| `outname` | output file name (excluding extension) | hpo_result | - |
| `to_json` | output result to a json file | False | - |
| `to_html` | output result to an html file | False | - |
| `to_csv` | output result to a csvle | False | - |
| `to_pcp` | output result as a parallel coordinate plot | False | - |

# Command Line Options
* To kill a job by jeditaskid
```
hpogrid tasks kill <jeditaskid>
```

* To retry a job by jeditaskid
```
hpogrid tasks retry <jeditaskid>
```

* To see a list of available GPU sites
```
hpogrid sites
```

# Important NOTES

### Working Directory of Container
* By default, the working directory (where the training scripts are located) of the container is `/hpogrid/project/`

### Location of Input Dataset
* By default, the location of input dataset inside the container is `/hpogrid/project/` (same as working directory)


### Digest of Grid Site Errors
* To be updated




