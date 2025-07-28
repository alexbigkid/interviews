#!/bin/bash

# e: stop if any errors
# u: Treat unset variables and parameters as an error
# set -eu

EXIT_CODE=0
EXPECTED_NUMBER_OF_PARAMS=0
COMMON_LIB_FILE="CommonLib.sh"
TERRAFORM_DIR="terraform"
# TERRAFORM_APPLY_TIMEOUT="10m"


#---------------------------
# functions
#---------------------------
PrintUsageAndExitWithCode() {
    echo
    echo "$0 deploys terraform infrastructure"
    echo "This script ($0) must be called with $EXPECTED_NUMBER_OF_PARAMS parameters."
    echo "  The AWS_DEFAULT_REGION environment variable needs to be set to: us-east-1, us-east-2, us-west-1 or us-west-2"
    echo "  The AWS_ACCESS_KEY_ID environment variable needs to be setup"
    echo "  The AWS_SECRET_ACCESS_KEY environment variable needs to be setup"
    echo
    echo "  $0 --help           - display this info"
    exit $1
}

DeployTerraform() {
    echo
    echo -e "${YELLOW}-> ${FUNCNAME[0]} ($@)${NC}"
    local LCL_PROJECT=$1
    local LCL_EXIT_CODE=0
    local LCL_PROJECT_NAME=$(basename $LCL_PROJECT)

    echo "terraforming project: $LCL_PROJECT_NAME"
    pushd $LCL_PROJECT
    terraform init -input=false || return $?
    terraform apply -input=false -auto-approve || return $?
    popd

    echo -e "${YELLOW}<- ${FUNCNAME[0]} ($LCL_EXIT_CODE)${NC}"
    echo
    return $LCL_EXIT_CODE
}

DeployTerraformProjects() {
    echo
    echo -e "${YELLOW}-> ${FUNCNAME[0]} ($@)${NC}"
    local LCL_ENV=$1
    local LCL_EXIT_CODE=0

    TERRAFORM_PROJECTS=$(ls -d $TERRAFORM_DIR/$LCL_ENV/[0-9][0-9][0-9]*/ | sort)
    echo
    echo "terraform projects found:"
    echo "$TERRAFORM_PROJECTS"

    for PROJECT in ${TERRAFORM_PROJECTS[@]}; do
        DeployTerraform $PROJECT || PrintUsageAndExitWithCode $EXIT_CODE_DEPLOYMENT_FAILED
    done

    echo -e "${YELLOW}<- ${FUNCNAME[0]} ($LCL_EXIT_CODE)${NC}"
    echo
    return $LCL_EXIT_CODE
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
echo -e "${GREEN}-> $0 ($@)${NC}"



IsParameterHelp $# $1 && PrintUsageAndExitWithCode $EXIT_CODE_SUCCESS
CheckNumberOfParameters $EXPECTED_NUMBER_OF_PARAMS $@ || PrintUsageAndExitWithCode $EXIT_CODE_INVALID_NUMBER_OF_PARAMETERS

[ "$ENV" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}ENV is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR
[ "$REGION" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}REGION is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR
[ "$AWS_ACCESS_KEY_ID" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}AWS_ACCESS_KEY_ID is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR
[ "$AWS_SECRET_ACCESS_KEY" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}AWS_SECRET_ACCESS_KEY is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR
[ "$AWS_DEFAULT_REGION" == "" ] && echo -e "${RED}ERROR:${NC} ${PURPLE}AWS_DEFAULT_REGION is not defined${NC}" && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR

IsPredefinedParameterValid $ENV "${ENV_ARRAY[@]}" || PrintUsageAndExitWithCode $EXIT_CODE_NOT_VALID_PARAMETER
IsPredefinedParameterValid $AWS_DEFAULT_REGION "${REGION_ARRAY[@]}" || PrintUsageAndExitWithCode $EXIT_CODE_NOT_VALID_PARAMETER

echo
echo -e "${YELLOW} configured terraform variables${NC}"
echo "------------------------------------------------"
# DO NOT PRINT on PIPPELINE, since there are sensitive info stored
# set | grep TF_

DeployTerraformProjects $ENV

echo -e "${GREEN}<- $0 ($EXIT_CODE)${NC}"
echo
exit $EXIT_CODE
