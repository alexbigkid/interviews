#!/bin/bash

#------------------------------------------------------------------------------
# variables definitions
#------------------------------------------------------------------------------
declare -r TRUE=0
declare -r FALSE=1
declare -a ENV_ARRAY=("dev" "qa" "prod")
declare -a REGION_ARRAY=("us-west-2")
GL_USERS_POOL_NAME="GlobalLogicUserPool"
GL_USERS_POOL_CLIENT_NAME="GlobalLogicAppClient"

#------------------------------------------------------------------------------
# Trace configuration
#------------------------------------------------------------------------------
TRACE_NONE=0
TRACE_ERROR=1
TRACE_CRITICAL=2
TRACE_WARNING=3
TRACE_FUNCTION=4
TRACE_INFO=5
TRACE_DEBUG=6
TRACE_ALL=7
TRACE_LEVEL=$TRACE_ALL


#------------------------------------------------------------------------------
# exit error codes
#------------------------------------------------------------------------------
EXIT_CODE_SUCCESS=0
EXIT_CODE_GENERAL_ERROR=1
EXIT_CODE_NOT_BASH_SHELL=2
EXIT_CODE_REQUIRED_TOOL_IS_NOT_INSTALLED=3
EXIT_CODE_INVALID_NUMBER_OF_PARAMETERS=4
EXIT_CODE_NOT_VALID_PARAMETER=5
EXIT_CODE_FILE_DOES_NOT_EXIST=6
EXIT_CODE_NOT_VALID_AWS_ACCOUNT_NUMBER=7
EXIT_CODE_ENV_VAR_NOT_VALID=8
EXIT_CODE_REGION_VAR_NOT_VALID=9
EXIT_CODE_INTEGRATION_TEST_FAILED=10
EXIT_CODE_DEPLOYMENT_FAILED=100
EXIT_CODE=$EXIT_CODE_SUCCESS


#------------------------------------------------------------------------------
# color definitions
#------------------------------------------------------------------------------
if [ -z "${GLOBALLOGIC_DISABLE_BASH_COLORS+x}" ] || [ -z "$GLOBALLOGIC_DISABLE_BASH_COLORS" ]; then
    BLK='\033[0;30m'
    RED='\033[0;31m'
    GRN='\033[0;32m'
    ORG='\033[0;33m'
    BLU='\033[0;34m'
    PRL='\033[0;35m'
    CYN='\033[0;36m'
    LGR='\033[0;37m'
    DGR='\033[1;30m'
    LRD='\033[1;31m'
    LGR='\033[1;32m'
    YLW='\033[1;33m'
    LBL='\033[1;34m'
    LPR='\033[1;35m'
    LCY='\033[1;36m'
    WHT='\033[1;37m'
    NC='\033[0m' # No Color
else
    echo "not using colors: GLOBALLOGIC_DISABLE_BASH_COLORS is defined: $GLOBALLOGIC_DISABLE_BASH_COLORS"
    BLK=
    RED=
    GRN=
    ORG=
    BLU=
    PRL=
    CYN=
    LGR=
    DGR=
    LRD=
    LGR=
    YLW=
    LBL=
    LPR=
    LCY=
    WHT=
    NC=
fi


#------------------------------------------------------------------------------
# unix type
#------------------------------------------------------------------------------
unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*) export GL_UNIX_TYPE=linux ;;
    Darwin*) export GL_UNIX_TYPE=mac ;;
    CYGWIN*) export GL_UNIX_TYPE=cygwin ;;
    MINGW*) export GL_UNIX_TYPE=mingw ;;
    *) GL_UNIX_TYPE="UNKNOWN:${unameOut}" ;;
esac


#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------
PrintTrace() {
    local LCL_TRACE_LEVEL=$1
    shift
    local LCL_PRINT_STRING=("$@")
    # shellcheck disable=SC2086
    if [ $TRACE_LEVEL -ge $LCL_TRACE_LEVEL ]; then
        case $LCL_TRACE_LEVEL in
            "$TRACE_CRITICAL")
                echo -e "${RED}[CRITICAL] ${LCL_PRINT_STRING[*]}${NC}" ;;
            "$TRACE_ERROR")
                echo -e "${RED}[ERROR] ${LCL_PRINT_STRING[*]}${NC}" ;;
            "$TRACE_WARNING")
                echo -e "${ORG}[WARNING] ${LCL_PRINT_STRING[*]}${NC}" ;;
            "$TRACE_FUNCTION")
                echo -e "${CYN}${LCL_PRINT_STRING[*]}${NC}" ;;
            "$TRACE_INFO")
                echo -e "${YLW}[INFO] ${LCL_PRINT_STRING[*]}${NC}" ;;
            "$TRACE_DEBUG")
                echo -e "${BLU}[DEBUG] ${LCL_PRINT_STRING[*]}${NC}" ;;
            *)
                echo -e "${LCL_PRINT_STRING[@]}" ;;
        esac
    fi
}


IsParameterHelp()
{
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local NUMBER_OF_PARAMETERS=$1
    local PARAMETER=$2
    if [[ $NUMBER_OF_PARAMETERS -eq 1 && $PARAMETER == "--help" ]]; then
        PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} (TRUE)"
        return $TRUE
    else
        PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} (FALSE)"
        return $FALSE
    fi
}


use_defined_variables() {
    # The purpose of this function is just to ensure that the definitions of all variables on the top of the file are used
    # Without this function shellcheck tool will bring up a lot of warnings of unused variables.
    # Even though some variables might not be used at the moment, they might be used in the future.
    # #shellcheck disable=SC2034 - was not used because it makes the variable definitions harder to read.
    PrintTrace $TRACE_ALL "use_defined_variables"
    PrintTrace $TRACE_NONE "$BLK $RED $GRN $ORG $BLU $PRL $CYN $LGR $DGR $LRD $LGR $YLW $LBL $LPR $LCY $WHT $NC"
    PrintTrace $TRACE_NONE "$EXIT_CODE_SUCCESS $EXIT_CODE_GENERAL_ERROR $EXIT_CODE_NOT_BASH_SHELL $EXIT_CODE_REQUIRED_TOOL_IS_NOT_INSTALLED $EXIT_CODE_INVALID_NUMBER_OF_PARAMETERS $EXIT_CODE_NOT_VALID_PARAMETER $EXIT_CODE_FILE_DOES_NOT_EXIST $EXIT_CODE_NOT_VALID_AWS_ACCOUNT_NUMBER $EXIT_CODE_ENV_VAR_NOT_VALID $EXIT_CODE_REGION_VAR_NOT_VALID $EXIT_CODE_INTEGRATION_TEST_FAILED $EXIT_CODE_DEPLOYMENT_FAILED $EXIT_CODE"
    PrintTrace $TRACE_NONE "$TRUE $FALSE"
    # shellcheck disable=SC2128
    PrintTrace $TRACE_NONE "$ENV_ARRAY $REGION_ARRAY $GL_USERS_POOL_NAME $GL_USERS_POOL_CLIENT_NAME"
}


CheckNumberOfParameters()
{
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_EXPECTED_NUMBER_OF_PARAMS=$1
    shift
    local LCL_PARAMETERS_PASSED_IN=("$@")
    # shellcheck disable=SC2086
    if [ $LCL_EXPECTED_NUMBER_OF_PARAMS -ne ${#LCL_PARAMETERS_PASSED_IN[@]} ]; then
        PrintTrace $TRACE_ERROR "invalid number of parameters."
        PrintTrace $TRACE_ERROR "  expected number:  $LCL_EXPECTED_NUMBER_OF_PARAMS"
        PrintTrace $TRACE_ERROR "  passed in number: ${#LCL_PARAMETERS_PASSED_IN[@]}"
        [ ${#LCL_PARAMETERS_PASSED_IN[@]} -ne 0 ] && PrintTrace $TRACE_ERROR "  parameters passed in: ${LCL_PARAMETERS_PASSED_IN[*]}"
        PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} (FALSE)"
        return $FALSE
    else
        PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} (TRUE)"
        return $TRUE
    fi
}


IsPredefinedParameterValid()
{
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local MATCH_FOUND=$FALSE
    local VALID_PARAMETERS=""
    local PARAMETER=$1
    shift
    local PARAMETER_ARRAY=("$@")
    PrintTrace $TRACE_DEBUG "PARAMETER = $PARAMETER"

    # shellcheck disable=SC2068
    for element in ${PARAMETER_ARRAY[@]}; do
        if [ "$PARAMETER" == "$element" ]; then
            MATCH_FOUND=$TRUE
        fi
        VALID_PARAMETERS="$VALID_PARAMETERS $element,"
        PrintTrace $TRACE_DEBUG "VALID PARAMS = $element"
    done

    if [ $MATCH_FOUND -eq $TRUE ]; then
        PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} (TRUE)"
        return $TRUE
    else
        PrintTrace $TRACE_ERROR "Invalid parameter: ${PRL}$PARAMETER${NC}"
        PrintTrace $TRACE_ERROR "Valid Parameters: $VALID_PARAMETERS"
        PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} (FALSE)"
        return $FALSE
    fi
}


CreateEnvConfigFile() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR=$1
    local LCL_ENV=$2
    local LCL_CFG_FILE=$3
    local LCL_EXIT_CODE=$EXIT_CODE_GENERAL_ERROR

    # check number of parameters and the config template exist
    if [ $# -eq 3 ] && [ -f "$LCL_CFG_FILE" ]; then
        # determine the config name for the environment
        local LCL_CFG_ARRAY=
        IFS='.' read -r -a LCL_CFG_ARRAY <<< "$LCL_CFG_FILE"
        local LCL_ENV_CFG_FILE="${LCL_CFG_ARRAY[0]}.$LCL_ENV.${LCL_CFG_ARRAY[1]}"
        PrintTrace $TRACE_DEBUG "LCL_CFG_ARRAY = ${LCL_CFG_ARRAY[*]}"
        PrintTrace $TRACE_DEBUG "LCL_ENV_CFG_FILE = $LCL_ENV_CFG_FILE"
        cp "$LCL_CFG_FILE" "$LCL_ENV_CFG_FILE"
        LCL_EXIT_CODE=$?
    fi

    eval "$LCL_RETURN_VAR"=\$LCL_ENV_CFG_FILE
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_ENV_CFG_FILE)"
    return $LCL_EXIT_CODE
}


WriteValueToConfigFile() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_ENV_CFG_FILE=$1
    local LCL_KEY=$2
    local LCL_VALUE=$3
    local LCL_EXIT_CODE=$EXIT_CODE_GENERAL_ERROR

    # check number of parameters and the env config exist
    if [ $# -eq 3 ] && [ -f "$LCL_ENV_CFG_FILE" ]; then
        PrintTrace $TRACE_DEBUG "LCL_ENV_CFG_FILE   = $LCL_ENV_CFG_FILE"
        PrintTrace $TRACE_DEBUG "LCL_KEY            = $LCL_KEY"
        PrintTrace $TRACE_DEBUG "LCL_VALUE          = $LCL_VALUE"
        if [ "$GL_UNIX_TYPE" = "mac" ]; then
            sed -i '' "s;\$${LCL_KEY};${LCL_VALUE};g" "$LCL_ENV_CFG_FILE"
            LCL_EXIT_CODE=$?
        elif [ "$GL_UNIX_TYPE" = "linux" ]; then
            sed -i "s;\$${LCL_KEY};${LCL_VALUE};g" "$LCL_ENV_CFG_FILE"
            LCL_EXIT_CODE=$?
        else
            PrintTrace $TRACE_ERROR "$GL_UNIX_TYPE is not supported"
        fi
    fi

    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE)"
    return $LCL_EXIT_CODE
}


GetCognitoUsersPoolId() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR=$1
    local LCL_USERS_POOL_NAME=$2
    local LCL_EXIT_CODE=0
    local LCL_USER_POOL_ID=
    LCL_USER_POOL_ID=$(aws cognito-idp list-user-pools --max-results=50 | jq -r ".UserPools[] | select(.Name==\"$LCL_USERS_POOL_NAME\") | .Id")
    PrintTrace $TRACE_DEBUG "LCL_USER_POOL_ID = $LCL_USER_POOL_ID"
    [ "$LCL_USER_POOL_ID" == "" ] && LCL_EXIT_CODE=1

    eval "$LCL_RETURN_VAR"=\$LCL_USER_POOL_ID
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_USER_POOL_ID)"
    return $LCL_EXIT_CODE
}


GetCognitoUserPoolClientId() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR=$1
    local LCL_USERS_POOL_ID=$2
    local LCL_USERS_POOL_CLIENT_NAME=$3
    local LCL_EXIT_CODE=0
    local LCL_USER_POOL_CLIENT_ID=

    LCL_USER_POOL_CLIENT_ID=$(aws cognito-idp list-user-pool-clients --user-pool-id "$LCL_USERS_POOL_ID" | jq -r ".UserPoolClients[] | select(.ClientName==\"$LCL_USERS_POOL_CLIENT_NAME\") | .ClientId")
    PrintTrace $TRACE_DEBUG "LCL_USER_POOL_CLIENT_ID = $LCL_USER_POOL_CLIENT_ID"
    [ "$LCL_USER_POOL_CLIENT_ID" == "" ] && LCL_EXIT_CODE=1

    eval "$LCL_RETURN_VAR"=\$LCL_USER_POOL_CLIENT_ID
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_USER_POOL_CLIENT_ID)"
    return $LCL_EXIT_CODE
}


GetCognitoIdToken() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR=$1
    local LCL_USER_POOL_CLIENT_ID=$2
    local LCL_EXIT_CODE=0
    local LCL_AUTH_COGNITO_ID_TOKEN=

    LCL_AUTH_COGNITO_ID_TOKEN=$(aws cognito-idp initiate-auth --auth-flow USER_PASSWORD_AUTH --auth-parameters USERNAME="$GL_COGNITO_USR",PASSWORD="$GL_COGNITO_PSW" --client-id "$LCL_USER_POOL_CLIENT_ID" --output text --query 'AuthenticationResult.IdToken')
    [ "$LCL_AUTH_COGNITO_ID_TOKEN" == "" ] && LCL_EXIT_CODE=1

    eval "$LCL_RETURN_VAR"=\$LCL_AUTH_COGNITO_ID_TOKEN
    # PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_AUTH_COGNITO_ID_TOKEN)"
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE)"
    return $LCL_EXIT_CODE
}


InstallRequiredServerlessPlugins() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_PLUGIN_LIST=

    LCL_PLUGIN_LIST=$(yq eval ".plugins[]" serverless.yml)
    if [ "$LCL_PLUGIN_LIST" != "" ]; then
        while IFS= read -r PLUGIN; do
            PrintTrace $TRACE_INFO "\n----------------------------------------\n$PLUGIN - installing ...\n----------------------------------------"
            serverless plugin install --name "$PLUGIN"
            echo "----------------------------------------------------------------------"
        done <<< "$LCL_PLUGIN_LIST"

    else
        PrintTrace $TRACE_CRITICAL "No serverless plugins to install"
    fi
    echo

    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} (0)"
    return 0
}


InstallExternalNodeDependencies() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_EXT_NODE_DEP_ARRAY=("$@")
    local LCL_EXIT_CODE=0

    # shellcheck disable=SC2068
    for dependency in ${LCL_EXT_NODE_DEP_ARRAY[@]}; do
        if [ -f "$dependency/package.json" ]; then
            (
                cd "$dependency" || exit $?
                PrintTrace $TRACE_INFO "Installing external node dependency: ${YLW}$dependency${NC}"
                npm install || exit $?
            ) || { PrintTrace $TRACE_ERROR "Failed to install dependency: $dependency"; LCL_EXIT_CODE=$?; }
        else
            PrintTrace $TRACE_ERROR "external node dependency file: '$dependency/package.json' does not exist$"
            LCL_EXIT_CODE=$EXIT_CODE_FILE_DOES_NOT_EXIST
        fi
    done

    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE)"
    return $LCL_EXIT_CODE
}

InstallPythonTestDependenciesIfRequired() {
    # This function is needed on the pipeline.
    # Python dependencies needs to be installed every time on the pipeline, since they will be missing.
    # However installing python dependencies on the local machine is not required.
    # This function checks whether a specific file exist on the file system.
    # If it does function assumes the we are running from a local machine
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_FILE_TO_CHECK=$1
    local LCL_PYTHON_DEPENDENCIES_FILE="requirements.txt"
    local LCL_EXIT_CODE=0

    if [ ! -f "$LCL_FILE_TO_CHECK" ] && [ -f "$LCL_PYTHON_DEPENDENCIES_FILE" ]; then
        pip install --upgrade setuptools
        pip install --requirement $LCL_PYTHON_DEPENDENCIES_FILE
    fi

    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE)"
    return $LCL_EXIT_CODE
}


GetServiceInvokeUrl() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR=$1
    local LCL_SERVICE_NAME=$2
    local LCL_ENV=$3
    local LCL_REGION=$4
    local LCL_SERVICE_INVOKE_URL=""
    local LCL_EXIT_CODE=0
    local LCL_REST_API_ID=

    LCL_REST_API_ID=$(aws apigateway get-rest-apis --region "$LCL_REGION" | jq -r ".items[] | select(.name==\"$LCL_SERVICE_NAME\") | .id")
    PrintTrace $TRACE_DEBUG "LCL_REST_API_ID = $LCL_REST_API_ID"
    if [ "$LCL_REST_API_ID" != "" ]; then
        LCL_SERVICE_INVOKE_URL="https://$LCL_REST_API_ID.execute-api.$LCL_REGION.amazonaws.com/$LCL_ENV"
    else
        LCL_EXIT_CODE=1
    fi

    eval "$LCL_RETURN_VAR"=\$LCL_SERVICE_INVOKE_URL
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_SERVICE_INVOKE_URL)"
    return $LCL_EXIT_CODE
}
