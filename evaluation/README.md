# Test Execution

This repository contains various tests to evaluate the project's functionalities. Follow the instructions below to run the tests and modify the VM parameters.

## Test 1: VM-as-a-service

### Execution

1. Open a terminal.
2. Navigate to the `evaluation` folder:
    ```sh
    cd evaluation
    ```
3. Run the `script_eval.sh` script specifying the number of repetitions:
    ```sh
    ./script_eval.sh 5
    ```

### Modifying RAM Parameters

1. **Modify `capacity_test_VM.py`**:
    - Change the directory names at lines 39, 67, 68, and 69 to the new RAM value (e.g., 2048 MB):
        ```python
        directory_response_time = "response_time_2048"
        ```

2. **Modify `script.sh`**:
    - Update line 44 to reflect the new RAM value (e.g., 2048 MB):
        ```sh
        config_string="deploy_honeypot2(config, \"$vm_name\", \"ubuntu/focal64\", \"2048\",\"shared\", 22, \"$free_port\",\"ssh\", \"$tap_name\", \"$mac_tap\", \"$ip_address\", $routes,\"$gateway\")"
        ```
## Test 2: Container-as-a-service

### Execution

1. Navigate to the `Honey-MTD-2/new_topology/lan1/vagrant/ubuntu` folder:
    ```sh
    cd Honey-MTD-2/new_topology/lan1/vagrant/ubuntu
    ```
2. Run `vagrant up ti_host1`:
    ```sh
    vagrant up ti_host1
    ```
3. Access the VM `ti_host1` through the VirtualBox GUI using the credentials `vagrant` / `vagrant`.
4. In the terminal of the VM, navigate to the `ti_host1/Evaluation` folder:
    ```sh
    cd ti_host1/Evaluation
    ```
5. Run the `script_eval.sh` script specifying the number of repetitions:
    ```sh
    ./script_eval.sh 5
    ```

### Modifying RAM Parameters for VM Running Containers

1. **Modify `ti_host1/Evaluation/capacity_test_Container.py`**:
    - Change the directory names at lines 36, 60, 61, and 62 to the new RAM value (e.g., 4096 MB):
        ```python
        directory_response_time = "response_time_4096"
        ```
