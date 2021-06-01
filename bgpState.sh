#!/bin/bash
#
while [ 0 ]; do
 date;
  for i in $(<target.list);
   do
    snmpwalk $i bgpPeerState |sed 's/^.*State\.//' |awk '{print $1,$4}' >$i.bgpState.current; 
    echo "$i BGP peer state change:"; 
    touch $i.bgpState.previous;
    diff $i.bgpState.previous $i.bgpState.current |sed -e 's/</ $i: Previous BGP state at $timestamp was:/' -e 's/>/ New BGP state is:/' |grep -v '^\-' >bgpState.result && mailx -s "BGP state change at $i" john.okey@host.com <bgpState.result ; 
    sleep 2; 
    mv $i.bgpState.current $i.bgpState.previous; 
    echo; 
  done; 
 echo " ---";
 sleep 5;
done
exit
