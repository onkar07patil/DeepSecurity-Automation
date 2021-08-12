# DeepSecurity-Automation
It is AWS auto-healing automation used for TrendMicro Deep Security.


There are 2 parts in this automation.
1. To install DS agent on newly created AWS instances.
2. To upgrade the agent to the latest version of agent during maintenance window.

Two lambdas:
1. TagforDSagentinstallation- keeps on communicating with the CloudOne console and checks if any new instances which are unmanaged i.e agent is not installed and tags them with the tag, windowsagentrequired/linuxagentrequired on the basis of platform.
2. UntagafterDSagentinstallation- Keeps on communicating with cloudone console and checks for managed instances and untags them and tag again as windowsagenyinstalled/linuxagentinstalled.

AgentInstallation CFT covers everything including all lambdas and System manager run commands to install agent on instances. Also System Manager run command is used in upgrading the agent to latest version.
