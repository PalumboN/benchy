# Table of Contents

- [Description](#description)
- [Benchmark Definition](#benchmark-definition)
- [Quick Start](#quick-start)
    - [Running all benchmarks](#running-all-benchmarks)
    - [Running options](#running-options)
    - [Output](#output)
- [Running your own benchmarks](#running-your-own-benchmarks)
    - [Parameters](#parameters)
    - [Executing your benchmars](#executing-your-benchmark) 
    - [Create your own configuration](#create-your-own-configuration)
- [Dependencies](#dependencies)
    - [Pharo Installation](#pharo-installation)
- [More info](#more-info)

# Description

Hello, I am an electric benchy, I can't go very fast or very far and if you drive me people will think you are awesome.

## Benchmark Definition

Each benchmark defines basically:

- In which images it need to be run
- With which vms
- and what code does the vm needs to evaluate to run the benchmark

One benchmark can be run on several images with several vms. Benchy will take care of that, you only need to specify the configuration.

# Quick Start

I am a framework for doing benchmarks in Pharo. 

## Running all benchmarks

Just run the `runAll.sh` script. That will:

1. Download all the pharo images that are defined in the `/images` folder
2. Then it will built the vms defined in the `/vms` folder
3. then it will run the benchmarks defined in the `benchs` folder

## Running options

Running `run.sh` will list options to run benchmarks.

To list the available benchmarks
`./run.sh list`

To run specific benchmarks in all images and all VMs
```bash
./run.sh bench slopstone
./run.sh bench richards
```

To plot existing results
`./run.sh bench plot`

## Output

Benchy will create a csv file with the time of the execution and two log files with the logs that happened during the execution. In your Pharo code you can to `anObj trace` to leave traces.

# Running your own benchmarks

## Parameters

It is possible to specify which directory containing benchmarks you want benchy to use. To do so, you must write `BENCHES_SCRIPT_DIR=<path to your directory> ./runAll.sh`. The path can be either relative or absolute. If not specified, `BENCHES_SCRIPT_DIR` is by default the `benchs` folder of benchy.

By default, benchy runs 30 iterations of each benchmarks. It is possible to customize this by using : `ITERATIONS=<number of your choice> ./runAll.sh`.  
For instance with `ITERATIONS=1 ./runAll.sh`, each benchmark will run once. 

You can also change the number of iterations locally. If you run `ITERATIONS=1 BENCHES_SCRIPT_DIR=myDir ./runAll.sh` with `myDir` being a directory containing several benchmarks, including the following one, it will run this benchmark file with 2 iterations but all the others with 1 iteration (look further down to see how to create benchmark configuration).

```bash
#!/bin/bash

# Configuration
IMAGES="Pharo11"
VMs="latest9"

# Command
PHARO_CMD="eval 1+1"

# Iterations
ITERATIONS=2

# Run
runBenchs
```
Note that if your number is 0 or less, benchy won't produce anything.

You can also add VM options when running `runAll.sh` with `VM_PARAMETERS=<parameter> ./runAll.sh`.  
Those options are available with `<vm> --help`. Like `ITERATIONS`, you can specify them locally. 

## Executing your benchmars

The benchmarks that are here by default are made to test the performance of Pharo. If you want to run your own benchmarks you need to:

1. Add a `.sh` file in the `/benchs` folder with the configuration of your benchmark.
2. [Optional] Add a `.sh` file in the `/vms` folder with the instructions to download your vm. If not you can use one of the already present vms.
3. Execute `runBenchs.sh name_of_your_benchmark` with the name.s of your benchmark.s

## Create your own configuration

You can create your own benchmark configuration by creating a `.sh` file using the following template:

```bash
#!/bin/bash

# Configuration
IMAGES="<the images you want your benchmark to run in>"
VMs="<the VMs you want your benchmark to run with>"

# Command
PHARO_CMD="<the command you want the VM to execute>"

# Run
runBenchs
```

and then add it to the `/benchs` folder.

You can also chain the following lines to run the same command with other images and/or VMs:

```bash
#!/bin/bash

# Command
PHARO_CMD="<the command you want the VM to execute>"

# First configuration
IMAGES="<the images you want your benchmark to run in>"
VMs="<the VMs you want your benchmark to run with>"

# Run
runBenchs


# Second configuration
IMAGES="<other images>"
VMs="<other VMs>"

# Iterations
ITERATIONS=3

# Run
runBenchs
```

Be sure not to forget to rewrite `runBenchs` so that the benchmark reruns with the new images and/or VMs.

# Dependencies

In order to run `benchParamTest.sh`, you need to download [shunit2](https://github.com/kward/shunit2) and add the path to the `shunit2` file to your `PATH`.

## Pharo Installation

```smalltalk
EpMonitor disableDuring: [ 
	Metacello new
		baseline: 'BenchHistory';
		repository: 'github://tesonep/benchy:main';
		load ]
```

# More info

In the `/src` folder there is code to make plots for the benchmarks.
