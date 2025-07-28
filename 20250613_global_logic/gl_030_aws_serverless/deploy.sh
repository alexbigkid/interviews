#!/bin/bash

EXIT_CODE=0
EXPECTED_NUMBER_OF_PARAMS=2
COMMON_LIB_FILE="./common-lib.sh"

PrintUsageAndExitWithCode ()
{
    echo
    echo "$0 run all scripts to create infrastructure"
    echo "This script ($0) must be called with $EXPECTED_NUMBER_OF_PARAMS parameters."
    echo "  1st parameter Environment: dev, qa or prod"
    echo "  2nd parameter Region: us-west-2 is supported at the moment"
    echo "  The AWS_ACCESS_KEY_ID environment variable needs to be setup"
    echo "  The AWS_SECRET_ACCESS_KEY environment variable needs to be setup"
    echo
    echo "  $0 --help           - display this info"
    echo
    echo -e "$2"
    # shellcheck disable=SC2086
    exit $1
}


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
# include common library, fail if does not exist
if [ -f $COMMON_LIB_FILE ]; then
# shellcheck disable=SC1091
# shellcheck source=../common-lib.sh
    source $COMMON_LIB_FILE
else
    echo "ERROR: $COMMON_LIB_FILE does not exist in the local directory."
    echo "  $COMMON_LIB_FILE contains common definitions and functions"
    exit 1
fi

echo
PrintTrace $TRACE_FUNCTION "-> $0 ($*)"


# ----------------------
# parameter validation
# ----------------------
IsParameterHelp $# "$1" && PrintUsageAndExitWithCode $EXIT_CODE_SUCCESS "---- Help displayed ----"
# shellcheck disable=SC2068
CheckNumberOfParameters $EXPECTED_NUMBER_OF_PARAMS $@ || PrintUsageAndExitWithCode $EXIT_CODE_INVALID_NUMBER_OF_PARAMETERS "${RED}ERROR: Invalid number of parameters${NC}"
IsPredefinedParameterValid "$1" "${ENV_ARRAY[@]}" || PrintUsageAndExitWithCode $EXIT_CODE_NOT_VALID_PARAMETER "${RED}ERROR: Invalid ENV parameter${NC}"
IsPredefinedParameterValid "$2" "${REGION_ARRAY[@]}" || PrintUsageAndExitWithCode $EXIT_CODE_NOT_VALID_PARAMETER "${RED}ERROR: Invalid REGION parameter${NC}"
[ "$AWS_ACCESS_KEY_ID" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: AWS_ACCESS_KEY_ID is not set${NC}"
[ "$AWS_SECRET_ACCESS_KEY" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: AWS_SECRET_ACCESS_KEY is not set${NC}"
[ "$GL_ENV" != "$1" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: $GL_ENV != $1\nPlease set ${GRN}GL_ENV${RED} in .envrc to ${GRN}$1${RED} to generate correct values in config.$1.yml${NC}"

GL_ENV=$1
GL_REGION=$2


#execute sub scripts
SCRIPT_FILES=$(ls [0-9][0-9][0-9]*.sh | sort)

echo "Execution scripts found:"
echo "$SCRIPT_FILES"

# shellcheck disable=SC2068
for SCRIPT in ${SCRIPT_FILES[@]}; do
    echo
    echo "about to execute $SCRIPT"
    "./$SCRIPT" "$GL_ENV" "$GL_REGION" || exit $?
done

PrintTrace $TRACE_FUNCTION "<- $0 ($EXIT_CODE)"
echo
exit $EXIT_CODE
