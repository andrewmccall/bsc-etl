# bsc ETL

[![Build Status](https://travis-ci.com/blockchain-etl/bsc-etl.png)](https://travis-ci.com/blockchain-etl/bsc-etl)
[![Join the chat at https://gitter.im/bsc-eth](https://badges.gitter.im/bsc-etl.svg)](https://gitter.im/bsc-etl/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Telegram](https://img.shields.io/badge/telegram-join%20chat-blue.svg)](https://t.me/joinchat/GsMpbA3mv1OJ6YMp3T5ORQ)
[![Discord](https://img.shields.io/badge/discord-join%20chat-blue.svg)](https://discord.gg/wukrezR)

BSC ETL lets you convert blockchain data into convenient formats like CSVs and relational databases.

[Full documentation available here](http://bsc-etl.readthedocs.io/).

## Quickstart

Install BSC ETL:

```bash
pip3 install bsc-etl
```

Export blocks and transactions ([Schema](docs/schema.md#blockscsv), [Reference](docs/commands.md#export_blocks_and_transactions)):

```bash
> bscetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
--blocks-output blocks.csv --transactions-output transactions.csv \
--provider-uri https://bsc-dataseed1.binance.org/v3/7aef3f0cd1f64408b163814b22cc643c
```

Export BEP20 transfers ([Schema](docs/schema.md#token_transferscsv), [Reference](docs/commands.md##export_token_transfers)):

```bash
> bscetl export_token_transfers --start-block 0 --end-block 500000 \
--provider-uri file://$HOME/Library/bsc/geth.ipc --output token_transfers.csv
```

Export traces ([Schema](docs/schema.md#tracescsv), [Reference](docs/commands.md#export_traces)):

```bash
> bscetl export_traces --start-block 0 --end-block 500000 \
--provider-uri file://$HOME/Library/bsc/parity.ipc --output traces.csv
```

---

Stream blocks, transactions, logs, token_transfers continually to console ([Reference](docs/commands.md#stream)):

```bash
> pip3 install bsc-etl[streaming]
> bscetl stream --start-block 500000 -e block,transaction,log,token_transfer --log-file log.txt \
--provider-uri https://bsc-dataseed1.binance.org/v3/7aef3f0cd1f64408b163814b22cc643c
```

Find other commands [here](https://bsc-etl.readthedocs.io/en/latest/commands/).

For the latest version, check out the repo and call 
```bash
> pip3 install -e . 
> python3 bscetl.py
```

## Useful Links

- [Schema](https://bsc-etl.readthedocs.io/en/latest/schema/)
- [Command Reference](https://bsc-etl.readthedocs.io/en/latest/commands/)
- [Documentation](https://bsc-etl.readthedocs.io/)
- [Public Datasets in BigQuery](https://github.com/blockchain-etl/public-datasets)  
- [Exporting the Blockchain](https://bsc-etl.readthedocs.io/en/latest/exporting-the-blockchain/)
- [Querying in Amazon Athena](https://bsc-etl.readthedocs.io/en/latest/amazon-athena/)
- [Querying in Google BigQuery](https://bsc-etl.readthedocs.io/en/latest/google-bigquery/)
- [Querying in Kaggle](https://www.kaggle.com/bigquery/bsc-blockchain)
- [Airflow DAGs](https://github.com/blockchain-etl/bsc-etl-airflow)
- [Postgres ETL](https://github.com/blockchain-etl/bsc-etl-postgresql)

## Running Tests

```bash
> pip3 install -e .[dev,streaming]
> export ETHEREUM_ETL_RUN_SLOW_TESTS=True
> export PROVIDER_URL=<your_porvider_uri>
> pytest -vv
``` 

### Running Tox Tests

```bash
> pip3 install tox
> tox
```

## Running in Docker

1. Install Docker: https://docs.docker.com/install/

2. Build a docker image
        
        > docker build -t bsc-etl:latest .
        > docker image ls
        
3. Run a container out of the image

        > docker run -v $HOME/output:/bscetl-etl/output bscetl-etl:latest export_all -s 0 -e 5499999 -b 100000 -p https://bsc-dataseed1.binance.org
        > docker run -v $HOME/output:/bscetl-etl/output bscetl-etl:latest export_all -s 2018-01-01 -e 2018-01-01 -p https://bsc-dataseed1.binance.org

4. Run streaming to console or Pub/Sub

        > docker build -t bsc-etl:latest -f Dockerfile .
        > echo "Stream to console"
        > docker run bscetl-etl:latest stream --start-block 500000 --log-file log.txt
        > echo "Stream to Pub/Sub"
        > docker run -v /path_to_credentials_file/:/bsc-etl/ --env GOOGLE_APPLICATION_CREDENTIALS=/bsc-etl/credentials_file.json bscetl-etl:latest stream --start-block 500000 --output projects/<your-project>/topics/crypto_bsc

## Projects using BSC ETL

** Add Some! ** 
