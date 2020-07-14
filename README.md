# Taurus

Taurus is a monitoring tool to deal with trading data sets

# Introduction

This projects aim to create monitoring and alerting as well as an best-effort market prediction, for stocks and indexes.


# Getting Started

# Project Constitution

- Python (3.6 or higher)
- Terraform (v0.12.16)
- Kubernetes ( in this case K3S cluster in Raspberry Pi rack)
- InfluxDB (1.7.10 or [latest](https://hub.docker.com/_/influxdb/))
- Grafana (v7.0.0-beta3  or [latest](https://hub.docker.com/r/grafana/grafana) )
- Postfix (TDB)


# To Do

- Create Tests!!!
- Create on-prem terraformed infra
- Create separated DB cluster ( InfluxDB )
- Create Grafana
- Create SMTP 
- Send Exports to InfluxDB
- Create REST API
- Add Swagger
- Breakdown app in processor and API
- Breakdown Terraform into namespaces for DB/Config/monitoring
- Apply [Benford's law](https://en.wikipedia.org/wiki/Benford%27s_law) for validation
- Does it needs [Black-scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)?
- Add TLS to DB connection
- Alerting Tool 


# Acknowledgements 
