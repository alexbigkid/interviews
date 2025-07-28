#!/bin/bash

# e: stop if any errors
# u: Treat unset variables and parameters as an error
# set -eu

EXIT_CODE=0
EXPECTED_NUMBER_OF_PARAMS=2
COMMON_LIB_FILE="common-lib.sh"
WORKING_DIR="services"
EXCLUDE_DIRS=( "gl-python-template" "gl-typescript-template" "serverless-template-ts" )

#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------
PrintUsageAndExitWithCode() {
    echo
    echo "$0 deploys lambdas in the services directory"
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

PublishService() {
    local LCL_YLW='\033[1;33m'
    local LCL_NC='\033[0m' # No Color
    echo
    echo -e "${LCL_YLW}-> ${FUNCNAME[0]} ($*)${LCL_NC}"
    local LCL_ENV=$1
    local LCL_REGION=$2
    local LCL_PROJECT=$3
    local LCL_EXIT_CODE=0
    local LCL_PROJECT_NAME=$(basename $LCL_PROJECT)

    if [ -e "${LCL_PROJECT}publish.sh" ]; then
        echo -e "deploying service project: ${LCL_YLW}$LCL_PROJECT_NAME${LCL_NC}"
        pushd $LCL_PROJECT
        ./publish.sh $LCL_ENV $LCL_REGION || LCL_EXIT_CODE=$?
        popd
    fi

    echo -e "${LCL_YLW}<- ${FUNCNAME[0]} ($LCL_PROJECT $LCL_EXIT_CODE)${LCL_NC}"
    echo
    return $LCL_EXIT_CODE
}
export -f PublishService

PublishServicesProjects() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_ENV=$1
    local LCL_REGION=$2
    local LCL_WORKING_DIR=$3
    local LCL_EXIT_CODE=0
    local LCL_SERVICE_PROJECTS=
    LCL_SERVICE_PROJECTS=$(ls -d $LCL_WORKING_DIR/*/ | grep -vFf <(printf "%s\n" "${EXCLUDE_DIRS[@]}") | sort)

    PrintTrace $TRACE_INFO "service projects found:"
    PrintTrace $TRACE_INFO "$LCL_SERVICE_PROJECTS"

    # for parallel deployment use this
    # ---------------------------------
    # parallel --halt now,fail=1 PublishService "$LCL_ENV" "$LCL_REGION" ::: "${LCL_SERVICE_PROJECTS[@]}"
    # LCL_EXIT_CODE=$?

    # Deploy services sequentially instead of in parallel to avoid conflicts
    # ---------------------------------
    for PROJECT in ${LCL_SERVICE_PROJECTS[@]}; do
        PublishService "$LCL_ENV" "$LCL_REGION" "$PROJECT" || LCL_EXIT_CODE=$?
        # Exit immediately if any service deployment fails
        if [ $LCL_EXIT_CODE -ne 0 ]; then
            PrintTrace $TRACE_ERROR "Service deployment failed for: $PROJECT"
            break
        fi
    done

    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE)"
    return $LCL_EXIT_CODE
}


#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------
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

PublishServicesProjects "$GL_ENV" "$GL_REGION" "$WORKING_DIR" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Services deployment failed${NC}"

PrintTrace $TRACE_FUNCTION "<- $0 ($EXIT_CODE)"
echo
exit $EXIT_CODE
