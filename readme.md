# How to use - A Genetic Algorithm for Student-Project Allocation (SPA) Problem
This GA allocates project to students and also considers students' preferences over projects, supervisors' capacity, workload and preferences 
over projects using NSGA-II. This algorithm has the ability to find optimal solutions for decision makers to make trade-off.

After the installation of GA package:

## How to set the parameters
There are five parameters that can be set by users.
1. pool_size: the number of population in every generation, it should be an integer.
2. mutation_rate: a float number between 0 and 1.
3. crossover_rate: a float number between 0 and 1.
4. max_generations: An integer, it max iteration times.
5. max_noImprovementCount: An integer, should be lower than max_generations

## To create a instance of GA
After setting up the parameters and [import data](https://github.com/suxingyu96/2023_SPA_GA#documentation), an instance of GA can be created.
```python
GA = SPA_genetic_algorithm(stu_list, proj_list, sup_list, 
                           pool_size, mutation_rate, 
                           crossover_rate, max_generations, 
                           max_noImprovementCount)
```

If you want to visualize the evolution process, create a new variable:
```python
visualization_screnn = True
```

## To execute the GA:
```python
pareto_solutions = GA.run()
GA.displayIndividuals(pareto_solutions)
```
When the GA is terminated, solutions belong to Pareto front will be returned to variable _**pareto_solutions**_ 
and displayed in the console.

# How to use the Benchmark tool
The benchmark tool is used to automate the performance tests of GA with different parameters.

## Tests with mutation rates
1. Create a list of mutation rates and set up other parameters:
```python
mutation_rate_list = [0.01, 0.025, 0.05, 0.1, 0.15]
pool_size = 600
crossover_rate = 0.8
max_generations = 1000
max_noImprovementCount = 100
```

2. Run the benchmark tool
 
```python
Benchmark.run_mutation_rates(stu_list, sup_list, proj_list, pool_size, 
                             mutation_rate_list, crossover_rate, 
                             max_generations, max_noImprovementCount)
```
When the benchmark terminates, a graph will show how GA performs as the Figure 5.1 in thesis.

## Tests with crossover rates
1. Create a list of crossover rates and set up other parameters:
```python
crossover_rates_list = [0.5, 0.8, 1]
pool_size = 600
mutation_rate = 0.01
max_generations = 1000
max_noImprovementCount = 100
```

2. Run the benchmark tool

```python
Benchmark.run_crossover_rates(stu_list, sup_list, proj_list, 
                              pool_size, mutation_rate, crossover_rates_list, 
                              max_generations, max_noImprovementCount)
```
When the benchmark terminates, a graph will show how GA performs as the Figure 5.2 in thesis.

## Tests with population sizes
1. Create a list of population sizes and set up other parameters:
```python
pool_sizes = [300, 600, 1000]
mutation_rate = 0.01
crossover_rate = 0.8
max_generations = 1000
max_noImprovementCount = 100
```

2. Run the benchmark tool

```python
Benchmark.run_population_sizes(stu_list, sup_list, proj_list, pool_sizes, 
                               mutation_rate, crossover_rate, max_generations, 
                               max_noImprovementCount)
```



