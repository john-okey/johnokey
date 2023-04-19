#!/bin/bash

# The main changes in this version are:
# The endless while loop has been replaced with a loop that reads the target list from a file. This 
# makes it easier to modify the list of targets without having to edit the script.
# The code that gets the current BGP peer state and checks for state changes has been broken down 
# into two separate functions: get_bgp_state() and check_bgp_state_change(). This improves the readability 
# of the code and makes it easier to modify or reuse these functions in other scripts.
# The for loop has been replaced with a while read loop that reads each target from the target.list file. 
# This avoids the need to parse the file using awk, which can be error-prone.
# Some minor changes have been made to improve the readability of the code, such as using descriptive 
# variable names and adding comments to explain what each part of the code does.

# To run the script:
# - Save the script code into a file with a .sh extension, such as bgp_state_checker.sh.
# - Make the file executable using the command chmod +x bgp_state_checker.sh.
# - Create a file called target.list in the same directory as the script and add the IP addresses or 
#   hostnames of the targets you want to check, one per line.
# - Run the script using the command ./bgp_state_checker.sh.
# - Note that the script assumes that the snmpwalk and mailx commands are installed on the system and that 
#   you have the necessary permissions to run them. If these commands are not available or you do not have 
#   the required permissions, you may need to modify the script or install the necessary packages.


# Function to get current BGP peer state
get_bgp_state() {
  local target=$1
  snmpwalk $target bgpPeerState | sed 's/^.*State\.//' | awk '{print $1,$4}' > $target.bgpState.current
}

# Function to check for BGP state change and send email notification
check_bgp_state_change() {
  local target=$1
  local timestamp=$(date)
  touch $target.bgpState.previous
  diff $target.bgpState.previous $target.bgpState.current \
    | sed -e "s/</$target: Previous BGP state at $timestamp was:/" -e 's/>/New BGP state is:/' \
    | grep -v '^\-' > bgpState.result \
    && mailx -s "BGP state change at $target" user@host.com < bgpState.result
  mv $target.bgpState.current $target.bgpState.previous
}

# Main loop
while read -r target; do
  date
  get_bgp_state "$target"
  echo "$target BGP peer state change:"
  check_bgp_state_change "$target"
  echo
  sleep 2
done < target.list

exit
