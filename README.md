Python script that automates the execution of commands on network devices using Paramiko for SSH connections and concurrent.futures for concurrent processing.


## Overview of the Script

The script performs the following tasks:

1. Establishes SSH connections to network devices.
2. Executes a list of commands on each device.
3. Saves the output of these commands to separate text files for each device.
4. Handles multiple devices concurrently using threading for better performance.
