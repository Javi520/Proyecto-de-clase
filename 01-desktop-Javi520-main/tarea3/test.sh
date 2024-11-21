#! /usr/bin/bash

Show_at_end=false
verbose=""

POSITIONAL=()
while (( $# > 0 )); do
    case "${1}" in
        -v|--verbose)
        Show_at_end=true
        verbose="-v"
        shift # shift once since flags have no values
        ;;
        -s|--switch)
        numOfArgs=1 # number of switch arguments
        if (( $# < numOfArgs + 1 )); then
            shift $#
        else
            echo "switch: ${1} with value: ${2}"
            shift $((numOfArgs + 1)) # shift 'numOfArgs + 1' to bypass switch and its value
        fi
        ;;
        *) # unknown flag/switch
        testnumber=${1}
        POSITIONAL+=("${1}")
        shift
        ;;
    esac
done

set -- "${POSITIONAL[@]}" # restore positional params

# Testing header
    printf '\r############# Testing \"watcher.py\" '
        sleep 0.5s
    printf '\r############# Testing \"watcher.py\".'
        sleep 0.5s
    printf '\r############# Testing \"watcher.py\"..'
        sleep 0.5s
    printf '\r############# Testing \"watcher.py\"...'
        sleep 0.5s
    printf "\n"

################ TEST 1 ###################

#./test_1.sh $verbose

################ TEST 2 ###################

#./test_2.sh $verbose

################ TEST 3 ###################

#./test_3.sh $verbose

################ TEST 4 # Tarea 4 #########

./test_4.sh $verbose