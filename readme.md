# A Genetic Algorithm for Student-Project Allocation (SPA) Problem
An algorithm in python that allocate project to students and also considers students' preferences over projects, supervisors' capacity, workload and preferences 
over projects using NSGA-II. This algorithm has the ability to find optimal solutions for decision makers to make trade-off.

## Installation
This tool needs Python 3.5 or above, and relies on `NumPy<http://www.numpy.org/>`.

You can install this by cloning from the repository:
```git 
$ git clone git@github.com:suxingyu96/2023_SPA_GA.git
$ cd 2023_SPA_GA
```
## Documentation 
This section contains the steps to execute this tool.

### Data import

This tool includes a DataReader to import data in **.txt** or **.csv** format from local files.

The data of students should be stored as:

| student ID | project 1  |  project 2 |  project 3 |project 4 | project 5 |
|------------|-----------:|-----------:|-----------:|---------:|----------:|


The data of supervisors should be stored as:

| supervisor ID | quota |project 1 | project 2 | project ... |
|-------|:----------|----------:|------------:|---------:|

The data of projects should be stored as:

| project ID | supervisor ID |
|-------|:----------|



The **DataReader** object generates lists from corresponding paths and check the validity of data.
```python
from objects.data_reader import DataReader
path_list = []
stu_data_path = str("path of students data file")
sup_data_path = str("path of supervisors data file")
proj_data_path = str("path of projects data file")

dataReader = DataReader(sup_data_path, stu_data_path, proj_data_path)

proj_list = dataReader.getProjectList()
sup_list = dataReader.getSupervisorList()
stu_list = dataReader.getStudentList()
```

### Run the GA
After creating the lists of data, it is time to run the GA. 

- Creating a **SPA_genetic_algorithm** instance and make the _lists_ as parameters and set the _population size_ and _mutation rate_, then the GA tool is initialized.
```python
from GeneticAlgorithm.SPA_genetic_algorithm import SPA_genetic_algorithm
population_size = 200
mutation_rate = 0.005
GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, population_size, mutation_rate)
```
- If you want to visualize the evolution process, set a variable **ParetoScreen** as **True**, or as **False** 
```python
ParetoScreen = True
```
- By calling the **.run(showParetoScreen)** to run the GA and a list of Pareto Optimal solutions will be returned after 
termination of the GA.
```python
pareto_solutions = GA.run(ParetoScreen)
```
- By calling the **.displayIndividuals(pareto_solutions)** method to display the detail of Pareto optimal solutions.
```python
GA.displayIndividuals(pareto_solutions)
```
