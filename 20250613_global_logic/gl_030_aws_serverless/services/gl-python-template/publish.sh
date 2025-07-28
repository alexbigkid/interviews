#!/bin/bash

# e: stop if any errors
# u: Treat unset variables and parameters as an error
# set -eu

EXIT_CODE=0
EXPECTED_NUMBER_OF_PARAMS=2
COMMON_LIB_FILE="../../common-lib.sh"
SERVICE_NAME=$(basename "$PWD")


#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------
PrintUsageAndExitWithCode() {
    echo
    echo "$0 deploys $SERVICE_NAME service"
    echo "This script ($0) must be called with $EXPECTED_NUMBER_OF_PARAMS parameters."
    echo "  1st parameter Environment: dev, qa or prod"
    echo "  2nd parameter Region: us-west-2 is supported at the momemnt"
    echo "  The AWS_ACCESS_KEY_ID environment variable needs to be setup"
    echo "  The AWS_SECRET_ACCESS_KEY environment variable needs to be setup"
    echo
    echo "  $0 --help           - display this info"
    echo
    echo -e "$2"
    # shellcheck disable=SC2086
    exit "$1"
}


RunUnitTests() {
    PrintTrace "$TRACE_FUNCTION" "-> ${FUNCNAME[0]} ()"

    PrintTrace "$TRACE_INFO" "Installing unit test dependencies ..."
    make install_test || return $?
    PrintTrace "$TRACE_INFO" "Running unit tests ..."
    make test_ff || return $?
    PrintTrace "$TRACE_INFO" "Running unit tests with coverage ..."
    make coverage || return $?

    PrintTrace "$TRACE_FUNCTION" "<- ${FUNCNAME[0]} (0)"
    return 0
}



#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
# include common library, fail if does not exist
if [ -f "$COMMON_LIB_FILE" ]; then
# shellcheck disable=SC1091
# shellcheck source=../common-lib.sh
    source "$COMMON_LIB_FILE"
else
    echo "ERROR: cannot find $COMMON_LIB_FILE"
    echo "  $COMMON_LIB_FILE contains common definitions and functions"
    exit 1
fi

echo
PrintTrace "$TRACE_FUNCTION" "-> $0 ($*)"

IsParameterHelp $# "$1" && PrintUsageAndExitWithCode "$EXIT_CODE_SUCCESS" "---- Help displayed ----"
# shellcheck disable=SC2068
CheckNumberOfParameters "$EXPECTED_NUMBER_OF_PARAMS" $@ || PrintUsageAndExitWithCode "$EXIT_CODE_INVALID_NUMBER_OF_PARAMETERS" "${RED}ERROR: Invalid number of parameters${NC}"
IsPredefinedParameterValid "$1" "${ENV_ARRAY[@]}" || PrintUsageAndExitWithCode "$EXIT_CODE_NOT_VALID_PARAMETER" "${RED}ERROR: Invalid parameter${NC}"
IsPredefinedParameterValid "$2" "${REGION_ARRAY[@]}" || PrintUsageAndExitWithCode "$EXIT_CODE_NOT_VALID_PARAMETER" "${RED}ERROR: Invalid REGION parameter${NC}"
[ "$AWS_ACCESS_KEY_ID" == "" ] && PrintUsageAndExitWithCode "$EXIT_CODE_GENERAL_ERROR" "${RED}ERROR: AWS_ACCESS_KEY_ID is not set${NC}"
[ "$AWS_SECRET_ACCESS_KEY" == "" ] && PrintUsageAndExitWithCode "$EXIT_CODE_GENERAL_ERROR" "${RED}ERROR: AWS_SECRET_ACCESS_KEY is not set${NC}"
[ "$GL_ENV" != "$1" ] && PrintUsageAndExitWithCode "$EXIT_CODE_GENERAL_ERROR" "${RED}ERROR: $GL_ENV != $1\nPlease set ${GRN}GL_ENV${RED} in .envrc to ${GRN}$1${RED} to generate correct values in config.$1.yml${NC}"

GL_ENV="$1"
GL_REGION="$2"

RunUnitTests || PrintUsageAndExitWithCode $? "${RED}ERROR: Failed unit tests${NC}"
InstallRequiredServerlessPlugins || PrintUsageAndExitWithCode $? "${RED}ERROR: Failed to install Serverless plugin${NC}"

PrintTrace "$TRACE_INFO" "Publishing service: ${YLW}$SERVICE_NAME${NC}"
serverless deploy --aws-profile "$GL_ENV" --stage "$GL_ENV" --region "$GL_REGION" || PrintUsageAndExitWithCode $? "${RED}ERROR: Failed to deploy service: $SERVICE_NAME${NC}"
PrintTrace "$TRACE_FUNCTION" "<- $0 ($EXIT_CODE)"
echo
exit "$EXIT_CODE"
