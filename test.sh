#!/bin/bash

# Start measuring time
start_time=$(date +%s)

echo "started"
# Calculate execution time
end_time=$(date +%s)
execution_time=$((end_time - start_time))

# Print the result
echo "Script execution time: $execution_time seconds"