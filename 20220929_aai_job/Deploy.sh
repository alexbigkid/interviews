#!/bin/bash

EXPECTED_NUMBER_OF_PARAMS=0
COMMON_LIB_FILE="./CommonLib.sh"

EXIT_CODE=0
PrintUsageAndExitWithCode ()
{
    echo
    echo "$0 run all scripts to create infrastructure"
    echo "This script ($0) must be called with $EXPECTED_NUMBER_OF_PARAMS parameters."
    echo "  The REGION environment variable needs to be set to: us-east-1, us-east-2 or us-west-2"
    echo "  The AWS_ACCESS_KEY_ID environment variable needs to be setup"
    echo "  The AWS_SECRET_ACCESS_KEY environment variable needs to be setup"
    echo
    echo "  $0 --help           - display this info"
    exit $1
}


# ----------
# main
# ----------
# include common library, fail if does not exist
if [ -f $COMMON_LIB_FILE ]; then
    source $COMMON_LIB_FILE
else
    echo "ERROR: $COMMON_LIB_FILE does not exist in the local directory."
    echo "  $COMMON_LIB_FILE contains common definitions and functions"
    exit 1
fi

echo
echo -e "${CYAN}-> $0 ($@)${NC}"


IsParameterHelp $# $1 && PrintUsageAndExitWithCode $EXIT_CODE_SUCCESS
CheckNumberOfParameters $EXPECTED_NUMBER_OF_PARAMS $@ || PrintUsageAndExitWithCode $EXIT_CODE_INVALID_NUMBER_OF_PARAMETERS

[ "$ENV" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}ENV is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR
[ "$REGION" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}REGION is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR
[ "$AWS_ACCESS_KEY_ID" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}AWS_ACCESS_KEY_ID is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR
[ "$AWS_SECRET_ACCESS_KEY" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}AWS_SECRET_ACCESS_KEY is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR


# validate env and region
IsPredefinedParameterValid $ENV "${ENV_ARRAY[@]}" || PrintUsageAndExitWithCode $EXIT_CODE_NOT_VALID_PARAMETER
IsPredefinedParameterValid $REGION "${REGION_ARRAY[@]}" || PrintUsageAndExitWithCode $EXIT_CODE_NOT_VALID_PARAMETER

#execute sub scripts
SCRIPT_FILES=$(ls [0-9][0-9][0-9]*.sh | sort)

echo "Execution scripts found:"
echo "$SCRIPT_FILES"

for SCRIPT in ${SCRIPT_FILES[@]}; do
    echo
    echo "about to execute $SCRIPT"
    ./$SCRIPT || exit $?
done

echo -e "${CYAN}<- $0 ($EXIT_CODE)${NC}"
echo
exit $EXIT_CODE
