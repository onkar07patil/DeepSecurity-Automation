#!/bin/bash

 /opt/ds_agent/dsa_control -r
 
 sleep 15
 
 /opt/ds_agent/dsa_control -a dsm://agents.deepsecurity.trendmicro.com:443/ "tenantID:B085ED1E-614B-A598-7D49-371C62B31DD2" "token:69B7883E-D11D-7799-2E0E-6E11F159C7B0"