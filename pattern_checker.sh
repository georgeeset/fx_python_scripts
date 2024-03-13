
#!/bin/bash

# check for price patterns and send alert to users.

echo $(date +%F" "%S)

mode="$1"


program_list=(
    "/home/gtwo/venvs/fx-scripts/bin/python3 /home/gtwo/docs/fx_python_scripts/yf_pattern_checker_service.py 2>> /var/log/yfx_pattern.log"
    "/home/gtwo/venvs/fx-scripts/bin/python3 /home/gtwo/docs/fx_python_scripts/crypto_pattern_checker_service.py 2>> /var/log/crypto_pattern.log"
    "/home/gtwo/venvs/fx-scripts/bin/python3 /home/gtwo/docs/fx_python_scripts/deriv_pattern_checker_service.py 2>> /var/log/deriv_pattern.log"
)

if [[ $mode == -l ]]; then
    program_list=(
    "/home/eset/venvs/fx-scripts/bin/python3 /home/eset/Documents/fx_python_scripts/yf_pattern_checker_service.py 2>> /var/log/yfx_pattern.log"
    "/home/eset/venvs/fx-scripts/bin/python3 /home/eset/Documents/fx_python_scripts/crypto_pattern_checker_service.py 2>> /var/log/crypto_pattern.log"
    "/home/eset/venvs/fx-scripts/bin/python3 /home/eset/Documents/fx_python_scripts/deriv_pattern_checker_service.py 2>> /var/log/deriv_pattern.log"
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
