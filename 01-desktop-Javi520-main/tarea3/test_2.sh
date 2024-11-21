#! /usr/bin/bash

Show_at_end=false

POSITIONAL=()
while (( $# > 0 )); do
    case "${1}" in
        -v|--verbose)
        Show_at_end=true
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

printf "executing \"test_view2.py\" file\n"

python3 ./test_view2.py > app_info_2.txt

printf "test complete... showing results\n"

printf "\n"
printf "#### TEST 2 RESULTS ####\n"
printf "\n"

cat tests_results_2.txt

printf "\n"

if ( $Show_at_end == true ); then
    cat app_info_2.txt
fi

printf "\n"