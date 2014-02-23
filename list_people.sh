#!/bin/bash

start_from="(manager=uid=lcongdon,ou=users,dc=redhat,dc=com)"

function lsearch() {
    # $1 should be a serch filter, anything else is extra fancyness for ldap search
    ldapsearch -xLLL $@ | awk '/^dn:/{print $2 "\n"}'
}

function sub_to_sup() {
    #1 = subordinate
    #2 = supervisor
    echo "$1 -> $2";
}

function reports_to(){
    # Give a DN to match people who have `manager` set to that
    PEOPLE=`mktemp`
    lsearch ${1} uid > ${PEOPLE}
    PEOPLE_COUNT=`grep -c 'uid' ${PEOPLE}`
    if [[ ${PEOPLE_COUNT} > 0 ]]; then
	echo "${PEOPLE_COUNT} report to ${1}"
    else
	echo "Nobody reports to ${1}"
    fi

}


reports_to $start_from


#lsearch $start_from uid



# Find PEOPLE who report to (`manager:`) PERSON                   (1)
#   If count(PEOPLE) == 0:
#     this person is a leaf node, not a boss
#   else:
#     this person is a vertex, they're sorta like a boss
#     for each PERSON in PEOPLE:
#       go to (1)
