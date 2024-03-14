#!/bin/bash

# find support/resistance and store in database

echo $(date +%F" "%T)

mode="$1"

program_list=(
    "/home/gtwo/venvs/fx-scripts/bin/python3 /home/gtwo/docs/fx_python_scripts/crypto_big_data_analyses.py 2>> /var/log/crypto_big_data.log"
    "/home/gtwo/venvs/fx-scripts/bin/python3 /home/gtwo/docs/fx_python_scripts/deriv_big_data_analyses.py 2>> /var/log/deriv_big_data.log"
    "/home/gtwo/venvs/fx-scripts/bin/python3 /home/gtwo/docs/fx_python_scripts/yf_big_data_analyses.py 2>> /var/log/yfx_big_data.log"
)

if [[ $mode == -l ]]; then
    program_list=(
    "/home/eset/venvs/fx-scripts/bin/python3 /home/eset/Documents/fx_python_scripts/crypto_big_data_analyses.py 2>> /var/log/crypto_big_data.log"
    "/home/eset/venvs/fx-scripts/bin/python3 /home/eset/Documents/fx_python_scripts/deriv_big_data_analyses.py 2>> /var/log/deriv_big_data.log"
    "/home/eset/venvs/fx-scripts/bin/python3 /home/eset/Documents/fx_python_scripts/yf_big_data_analyses.py 2>> /var/log/yfx_big_data.log"
    )
fi

# Iterate through each script
for program in "${program_list[@]}"; do
    echo "Running $program..."

    # Start measuring time
    start_time=$(date +%s)

    # Run your Python script (replace 'your_script.py' with the actual script name)
    $program

    # Calculate execution time
    end_time=$(date +%s)
    execution_time=$((end_time - start_time))

    # Print the result
    echo "Script execution time: $execution_time seconds"
done
