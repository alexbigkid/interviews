#! /bin/bash

COMMON_LIB_FILE="CommonLib.sh"
[ -f $COMMON_LIB_FILE ] && source $COMMON_LIB_FILE

#---------------------------
# functions
#---------------------------
InstallRequiredToolsUsingBrew ()
{
    local TOOL=(
                    aws
                    parallel
                    # serverless
                    terraform
                )
    local PACKAGE=(
                    awscli
                    parallel
                    # serverless
                    terraform
                  )
    echo
    echo -e "${GREEN}----------------------------------------------------------------------${NC}"
    echo -e "${GREEN}| ${FUNCNAME[0]}${NC}"
    echo -e "${GREEN}----------------------------------------------------------------------${NC}"

    for (( i = 0; i < ${#TOOL[@]}; i++)); do
        echo -e "\n------------------------\n${TOOL[$i]} - INSTALL AND CHECK\n------------------------"
        [ "$(command -v ${TOOL[$i]})" == "" ] && brew install ${PACKAGE[$i]} || which ${TOOL[$i]}
        echo -e "\n------------------------\n${TOOL[$i]} - VERSION\n------------------------"
        ${TOOL[$i]} --version || exit $?
        echo -e "${YELLOW}----------------------------------------------------------------------${NC}"
        echo
    done
}

InstallRequiredToolsUsingNpm ()
{
    local TOOL=(
                    serverless
                )
    local PACKAGE=(
                    serverless
                  )
    echo
    echo -e "${GREEN}----------------------------------------------------------------------${NC}"
    echo -e "${GREEN}| ${FUNCNAME[0]}${NC}"
    # echo -e "${YELLOW}| Please use this function if the installation of required tool fails with InstallRequiredToolsUsingBrew.${NC}"
    echo -e "${GREEN}----------------------------------------------------------------------${NC}"

    for (( i = 0; i < ${#TOOL[@]}; i++)); do
        echo -e "\n------------------------\n${TOOL[$i]} - INSTALL AND CHECK\n------------------------"
        [ "$(command -v ${TOOL[$i]})" == "" ] && sudo npm -g install ${PACKAGE[$i]} || which ${TOOL[$i]}
        echo -e "\n------------------------\n${TOOL[$i]} - VERSION\n------------------------"
        ${TOOL[$i]} --version || exit $?
        echo -e "${YELLOW}----------------------------------------------------------------------${NC}"
        echo
    done
}

#---------------------------
# main
#---------------------------
echo
echo "-> $0 ($@)"

InstallRequiredToolsUsingBrew || exit $?
InstallRequiredToolsUsingNpm || exit $?

echo "<- $0 (0)"
echo
exit 0
