#!/bin/bash

# e: stop if any errors
# u: Treat unset variables and parameters as an error
# set -eu

EXIT_CODE=0
EXPECTED_NUMBER_OF_PARAMS=2
COMMON_LIB_FILE="common-lib.sh"
CONFIG_FILE="config.yml"
GL_USERS_POOL_NAME="GlobalLogicUserPool"
TERRAFORM_ENVS_DIR="terraform"

#------------------------------------------------------------------------------
# functions
#------------------------------------------------------------------------------
PrintUsageAndExitWithCode() {
    echo
    echo "$0 setups environment configuration"
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


GetCognitoUsersPoolArn() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR=$1
    local LCL_USERS_POOL_NAME=$2
    local LCL_EXIT_CODE=0

    local LCL_USER_POOL_ID
    LCL_USER_POOL_ID=$(aws cognito-idp list-user-pools --max-results=50 | jq -r ".UserPools[] | select(.Name==\"$LCL_USERS_POOL_NAME\") | .Id")
    local LCL_USERPOOL_ARN
    LCL_USERPOOL_ARN=$(aws cognito-idp describe-user-pool --user-pool-id="$LCL_USER_POOL_ID" | jq -r '.UserPool.Arn')
    [ "$LCL_USERPOOL_ARN" == "" ] && LCL_EXIT_CODE=1

    eval $LCL_RETURN_VAR=\$LCL_USERPOOL_ARN
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_USERPOOL_ARN)"
    return $LCL_EXIT_CODE
}

GetRetainUntilTimestamp() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR=$1
    local LCL_EXIT_CODE=0
    local LCL_RETAIN_UNTIL_TIMESTAMP=""
    local LCL_TIME_UNIT_TO_ADD="8"
    local LCL_UNAME
    LCL_UNAME=$(uname -s)

    case "$LCL_UNAME" in
        Linux*) LCL_RETAIN_UNTIL_TIMESTAMP=$(date -d "+${LCL_TIME_UNIT_TO_ADD}mins" -u +"%FT%TZ") ;;
        # M - minutes, H - hours, d - days, m - months, y - years
        Darwin*) LCL_RETAIN_UNTIL_TIMESTAMP=$(date -v "+${LCL_TIME_UNIT_TO_ADD}M" -u +"%FT%TZ") ;;
        *) PrintTrace $TRACE_ERROR "${RED}ERROR: ${LCL_UNAME} not supported${NC}" ;;
    esac

    eval $LCL_RETURN_VAR=\$LCL_RETAIN_UNTIL_TIMESTAMP
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_RETAIN_UNTIL_TIMESTAMP)"
    return $LCL_EXIT_CODE
}


GetVpcSecurityGroupId() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR=$1
    local LCL_EXIT_CODE=0

    # TODO: the lambda VPC security group should be called the same way in dev, qa and prod
    local LCL_VPC_SECURITY_GROUP_ID
    LCL_VPC_SECURITY_GROUP_ID=$(aws ec2 describe-security-groups | jq -r '.SecurityGroups[] | select(.GroupName | startswith("lambda-security")) | .GroupId')
    [ "$LCL_VPC_SECURITY_GROUP_ID" == "" ] && LCL_EXIT_CODE=1

    eval $LCL_RETURN_VAR=\$LCL_VPC_SECURITY_GROUP_ID
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_VPC_SECURITY_GROUP_ID)"
    return $LCL_EXIT_CODE
}


GetVpcSubnetIds() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_RETURN_VAR1=$1
    local LCL_RETURN_VAR2=$2
    local LCL_RETURN_VAR3=$3
    local LCL_EXIT_CODE=0
    local LCL_VPC_SUBNET_IDS_JSON
    local LCL_VPC_SUBNET_ID1
    local LCL_VPC_SUBNET_ID2
    local LCL_VPC_SUBNET_ID3

    LCL_VPC_SUBNET_IDS_JSON=$(aws ec2 describe-subnets)
    # PrintTrace $TRACE_DEBUG "LCL_VPC_SUBNET_IDS_JSON = $LCL_VPC_SUBNET_IDS_JSON"
    [ "$LCL_VPC_SUBNET_IDS_JSON" == "" ] && LCL_EXIT_CODE=1


    LCL_VPC_SUBNET_ID1=$(jq -r '.Subnets[] | try(select(.Tags[].Value=="lambda-subnet-point-to-nat-1")) | .SubnetId' <<< $LCL_VPC_SUBNET_IDS_JSON)
    LCL_VPC_SUBNET_ID2=$(jq -r '.Subnets[] | try(select(.Tags[].Value=="lambda-subnet-point-to-nat-2")) | .SubnetId' <<< $LCL_VPC_SUBNET_IDS_JSON)
    LCL_VPC_SUBNET_ID3=$(jq -r '.Subnets[] | try(select(.Tags[].Value=="lambda-subnet-point-to-nat-3")) | .SubnetId' <<< $LCL_VPC_SUBNET_IDS_JSON)
    PrintTrace $TRACE_DEBUG "LCL_VPC_SUBNET_ID1 = $LCL_VPC_SUBNET_ID1"
    PrintTrace $TRACE_DEBUG "LCL_VPC_SUBNET_ID2 = $LCL_VPC_SUBNET_ID2"
    PrintTrace $TRACE_DEBUG "LCL_VPC_SUBNET_ID3 = $LCL_VPC_SUBNET_ID3"
    [ "$LCL_VPC_SUBNET_ID1" == "" ] && LCL_EXIT_CODE=1
    [ "$LCL_VPC_SUBNET_ID2" == "" ] && LCL_EXIT_CODE=1
    [ "$LCL_VPC_SUBNET_ID3" == "" ] && LCL_EXIT_CODE=1

    eval "$LCL_RETURN_VAR1"=\$LCL_VPC_SUBNET_ID1
    eval "$LCL_RETURN_VAR2"=\$LCL_VPC_SUBNET_ID2
    eval "$LCL_RETURN_VAR3"=\$LCL_VPC_SUBNET_ID3
    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE $LCL_VPC_SUBNET_ID1 $LCL_VPC_SUBNET_ID2 $LCL_VPC_SUBNET_ID3)"
    return $LCL_EXIT_CODE
}


SetupTerraformVariables() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_PROJECT=$1
    local LCL_ENV=$2
    local LCL_ENV_CONFIG="config.$LCL_ENV.yml"
    local LCL_TF_VARS_FILE="$LCL_PROJECT/terraform.tfvars.json"
    local LCL_EXIT_CODE=0

    local LCL_PROJECT_NAME
    LCL_PROJECT_NAME=$(basename $LCL_PROJECT)
    # splitting last directory by '_' to get just the last part and strip off the number in front
    local LCL_TERRAFORM_PRJ=(${LCL_PROJECT_NAME//_/ })
    PrintTrace $TRACE_DEBUG "LCL_TERRAFORM_PRJ[1] = ${LCL_TERRAFORM_PRJ[1]}"

    # parse config yaml file only for the project related settings
    local LCL_PROJECT_TF_VARS_JSON
    
    # Skip terraform.tfvars.json generation for postgreDB (uses TF_VAR_* env vars instead)
    if [ "${LCL_TERRAFORM_PRJ[1]}" = "postgreDB" ]; then
        LCL_PROJECT_TF_VARS_JSON="{}"
        PrintTrace $TRACE_DEBUG "Skipping terraform vars for postgreDB project"
    else
        LCL_PROJECT_TF_VARS_JSON=$(yq -o=json .terraform.${LCL_TERRAFORM_PRJ[1]} $LCL_ENV_CONFIG)
        PrintTrace $TRACE_DEBUG "LCL_PROJECT_TF_VARS_JSON = $LCL_PROJECT_TF_VARS_JSON"
    fi

    # write env configurated terraform vars file to project directory
    printf "%s" "$LCL_PROJECT_TF_VARS_JSON" > "$LCL_TF_VARS_FILE"

    PrintTrace $TRACE_FUNCTION "<- ${FUNCNAME[0]} ($LCL_EXIT_CODE)"
    return $LCL_EXIT_CODE
}


SetupTerraformProjects() {
    PrintTrace $TRACE_FUNCTION "-> ${FUNCNAME[0]} ($*)"
    local LCL_WORKING_DIR=$1
    local LCL_ENV=$2
    local LCL_EXIT_CODE=0
    local LCL_TERRAFORM_PROJECTS
    LCL_TERRAFORM_PROJECTS=$(ls -d $LCL_WORKING_DIR/$LCL_ENV/[0-9][0-9][0-9]*/ | sort)

    PrintTrace $TRACE_INFO "terraform projects found:"
    PrintTrace $TRACE_INFO "$LCL_TERRAFORM_PROJECTS"

    # shellcheck disable=SC2068
    for PROJECT in ${LCL_TERRAFORM_PROJECTS[@]}; do
        SetupTerraformVariables $PROJECT $LCL_ENV || LCL_EXIT_CODE=$?
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
[ "$GL_PRJ_NAME" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: GL_PRJ_NAME is not set${NC}"
[ "$GL_DB_USR" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: GL_DB_USR is not set${NC}"
[ "$GL_DB_PSW" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: GL_DB_PSW is not set${NC}"
[ "$GL_DB_HOST" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: GL_DB_HOST is not set${NC}"
[ "$GL_DB_PORT" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: GL_DB_PORT is not set${NC}"
[ "$GL_DB_NAME" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: GL_DB_NAME is not set${NC}"
[ "$LOG_LEVEL" == "" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: LOG_LEVEL is not set${NC}"
[ "$GL_ENV" != "$1" ] && PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: $GL_ENV != $1\nPlease set ${GRN}GL_ENV${RED} in .envrc to ${GRN}$1${RED} to generate correct values in config.$1.yml${NC}"

GL_ENV=$1
GL_REGION=$2

CreateEnvConfigFile ENV_CONFIG_FILE "$GL_ENV" "$CONFIG_FILE" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to create config file for env: $GL_ENV${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_ENV "$GL_ENV" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_ENV: $GL_ENV to config file${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_REGION "$GL_REGION" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_ENV: $GL_REGION to config file${NC}"

# GetCognitoUsersPoolArn GL_USERS_POOL_ARN "$GL_USERS_POOL_NAME" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Could not find ARN for $GL_USERS_POOL_NAME ${NC}"
# WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_USERS_POOL_ARN "$GL_USERS_POOL_ARN" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_USERS_POOL_ARN: $GL_USERS_POOL_ARN to config file${NC}"

GetRetainUntilTimestamp GL_CERT_VALID_UNTIL_DATE_TIME || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to generate: GL_CERT_VALID_UNTIL_DATE_TIME${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_CERT_VALID_UNTIL_DATE_TIME "$GL_CERT_VALID_UNTIL_DATE_TIME" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_CERT_VALID_UNTIL_DATE_TIME: $GL_CERT_VALID_UNTIL_DATE_TIME to config file${NC}"

# GetVpcSecurityGroupId GL_VPC_SECURITY_GROUP_ID || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to get: GL_VPC_SECURITY_GROUP_ID${NC}"
# WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_VPC_SECURITY_GROUP_ID "$GL_VPC_SECURITY_GROUP_ID" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_VPC_SECURITY_GROUP_ID: $GL_VPC_SECURITY_GROUP_ID to config file${NC}"

# GetVpcSubnetIds GL_VPC_SUBNET_ID1 GL_VPC_SUBNET_ID2 GL_VPC_SUBNET_ID3 || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to get: GL_VPC_SUBNET_IDS${NC}"
# WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_VPC_SUBNET_ID1 "$GL_VPC_SUBNET_ID1" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_VPC_SUBNET_ID1: $GL_VPC_SUBNET_ID1 to config file${NC}"
# WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_VPC_SUBNET_ID2 "$GL_VPC_SUBNET_ID2" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_VPC_SUBNET_ID2: $GL_VPC_SUBNET_ID2 to config file${NC}"
# WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_VPC_SUBNET_ID3 "$GL_VPC_SUBNET_ID3" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_VPC_SUBNET_ID3: $GL_VPC_SUBNET_ID3 to config file${NC}"

WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_PRJ_NAME "$GL_PRJ_NAME" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_PRJ_NAME: $GL_PRJ_NAME to config file${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_DB_USR "$GL_DB_USR" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_DB_USR: $GL_DB_USR to config file${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_DB_PSW "$GL_DB_PSW" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_DB_PSW: $GL_DB_PSW to config file${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_DB_HOST "$GL_DB_HOST" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_DB_HOST: $GL_DB_HOST to config file${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_DB_PORT "$GL_DB_PORT" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_DB_PORT: $GL_DB_PORT to config file${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_DB_NAME "$GL_DB_NAME" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_DB_NAME: $GL_DB_NAME to config file${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" GL_DB_CONN "$GL_DB_CONN" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write GL_DB_CONN: $GL_DB_CONN to config file${NC}"
WriteValueToConfigFile "$ENV_CONFIG_FILE" LOG_LEVEL "$LOG_LEVEL" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Failed to write LOG_LEVEL: $LOG_LEVEL to config file${NC}"


SetupTerraformProjects "$TERRAFORM_ENVS_DIR" "$GL_ENV" || PrintUsageAndExitWithCode $EXIT_CODE_GENERAL_ERROR "${RED}ERROR: Setup Terraform Projects failed${NC}"

PrintTrace $TRACE_FUNCTION "<- $0 ($EXIT_CODE)"
echo
exit $EXIT_CODE
