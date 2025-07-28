#!/bin/bash

# e: stop if any errors
# u: Treat unset variables and parameters as an error
set -eu

EXIT_CODE=0
EXPECTED_NUMBER_OF_PARAMS=2
COMMON_LIB_FILE="../common-lib.sh"
TEMPLATE_NAME_FOR_TYPESCRIPT="gl-typescript-template"
TEMPLATE_NAME_FOR_PYTHON="gl-python-template"
declare -a SUPPORTED_TYPES_ARRAY=("py" "ts")

TS_NODE_DEPENDENCIES=(
    '@alwaysai/common-cloud-infrastructure'
)
TS_NODE_DEV_DEPENDENCIES=(
    '@alwaysai/eslint-config'
    '@jest/globals'
    '@types/aws-lambda'
    '@types/jest'
    '@types/jsonwebtoken'
    '@types/node'
    '@types/pg'
    'esbuild'
    'jest'
    'serverless@^3.0.0'
    'serverless-deployment-bucket'
    'serverless-domain-manager'
    'serverless-esbuild'
    'serverless-latest-layer-version'
    'serverless-prune-plugin'
    'ts-jest'
    'ts-mock-imports'
    'typescript@~5.1.0'
)

PY_NODE_DEV_DEPENDENCIES=(
    'serverless-deployment-bucket'
    'serverless-domain-manager'
    'serverless-iam-roles-per-function'
    'serverless-prune-plugin'
    'serverless-python-requirements'
)


#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------
PrintUsageAndExitWithCode() {
    echo
    echo "$0 creates service from a template"
    echo "This script ($0) must be called with $EXPECTED_NUMBER_OF_PARAMS parameters."
    echo "  1st parameter type: py (python) or ts (TypeScript)"
    echo "  2nd parameter service name: should be kebab-case-name and not taken by previously created service"
    echo
    echo "  $0 --help           - display this info"
    echo -e "$2"
    exit "$1"
}

InstallNodeDependencies() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_SERVICE_TYPE="$1"
    local LCL_SERVICE_NAME="$2"
    local LCL_EXIT_CODE=0

    if [ ! -d "$LCL_SERVICE_NAME" ]; then
        PrintTrace $TRACE_ERROR "Directory does not exist: $LCL_SERVICE_NAME"
        return 1
    fi

    (
        cd "$LCL_SERVICE_NAME" || { PrintTrace $TRACE_INFO "Failed to change directory to $LCL_SERVICE_NAME"; exit $?; }
        PrintTrace $TRACE_INFO "PWD = $PWD"
        if [ "$LCL_SERVICE_TYPE" == "ts" ]; then
            PrintTrace $TRACE_INFO "installing node dependencies"
            npm install --save "${TS_NODE_DEPENDENCIES[@]}"

            PrintTrace $TRACE_INFO "installing node devDependencies"
            npm install --save --save-dev "${TS_NODE_DEV_DEPENDENCIES[@]}"
        else
            PrintTrace $TRACE_INFO "installing node devDependencies"
            npm install --save --save-dev "${PY_NODE_DEV_DEPENDENCIES[@]}"
            
            PrintTrace "$TRACE_INFO" "setting up uv environment for Python service"
            if command -v uv >/dev/null 2>&1; then
                PrintTrace "$TRACE_INFO" "initializing uv sync for dependencies"
                uv sync || PrintTrace "$TRACE_WARNING" "uv sync failed, falling back to pip install"
                
                PrintTrace "$TRACE_INFO" "generating initial requirements.txt for deployment"
                uv export --format requirements-txt --output-file requirements.txt --no-dev || PrintTrace "$TRACE_WARNING" "Failed to export requirements.txt"
            else
                PrintTrace "$TRACE_WARNING" "uv not found, please install uv for optimal local development"
                PrintTrace "$TRACE_INFO" "falling back to pip installation"
                pip install -r requirements.txt || PrintTrace "$TRACE_ERROR" "pip install failed"
            fi
        fi
    ) || LCL_EXIT_CODE=$?
    PrintTrace "$TRACE_INFO" "PWD = $PWD"

    PrintTrace "$TRACE_FUNCTION" "<- ${FUNCNAME[$LCL_EXIT_CODE]}"
    return $LCL_EXIT_CODE
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
[ $# -eq 0 ] && PrintUsageAndExitWithCode "$EXIT_CODE_SUCCESS" "${GRN}Did that help?${NC}"
IsParameterHelp $# "$1" && PrintUsageAndExitWithCode "$EXIT_CODE_SUCCESS" "${GRN}Did that help?${NC}"
# shellcheck disable=SC2068
CheckNumberOfParameters $EXPECTED_NUMBER_OF_PARAMS $@ || PrintUsageAndExitWithCode "$EXIT_CODE_INVALID_NUMBER_OF_PARAMETERS" "${RED}ERROR: Invalid number of parameters.${NC}"
IsPredefinedParameterValid "$1" "${SUPPORTED_TYPES_ARRAY[@]}" || PrintUsageAndExitWithCode "$EXIT_CODE_NOT_VALID_PARAMETER" "${RED}ERROR: Service type have to be 'py' or 'ts'.${NC}"

SERVICE_TYPE=$1
SERVICE_NAME=$2

[ -d "$SERVICE_NAME" ] && PrintUsageAndExitWithCode "$EXIT_CODE_NOT_VALID_PARAMETER" "${RED}ERROR: Service name already exist. Please choose another name.${NC}"
[ "$SERVICE_TYPE" = "py" ] && TEMPLATE_NAME=$TEMPLATE_NAME_FOR_PYTHON || TEMPLATE_NAME=$TEMPLATE_NAME_FOR_TYPESCRIPT
serverless create --template-path "$TEMPLATE_NAME" --name "$SERVICE_NAME" --path "$SERVICE_NAME"

# Replace placeholders in Python service files
if [ "$SERVICE_TYPE" = "py" ]; then
    PrintTrace "$TRACE_INFO" "Updating service configuration for $SERVICE_NAME"
    
    # Update pyproject.toml
    if [ -f "$SERVICE_NAME/pyproject.toml" ]; then
        sed -i.bak "s/{{SERVICE_NAME}}/$SERVICE_NAME/g" "$SERVICE_NAME/pyproject.toml"
        sed -i.bak "s/{{SERVICE_DESCRIPTION}}/GL $SERVICE_NAME Service/g" "$SERVICE_NAME/pyproject.toml"
        rm "$SERVICE_NAME/pyproject.toml.bak"
    fi
fi

InstallNodeDependencies "$SERVICE_TYPE" "$SERVICE_NAME" || EXIT_CODE=$?

PrintTrace "$TRACE_FUNCTION" "<- $0 ($EXIT_CODE)"
echo
exit $EXIT_CODE
