# Konfigurasi
from dotenv import load_dotenv
import os 
from sqlalchemy import text

load_dotenv()

SOURCE_SSH_USER=os.getenv('SOURCE_SSH_USER')
SOURCE_SSH_PASS=os.getenv('SOURCE_SSH_PASS')
SOURCE_SSH_HOST=os.getenv('SOURCE_SSH_HOST')
SOURCE_SSH_PORT=int(os.getenv('SOURCE_SSH_PORT'))
SOURCE_REMOTE_BIND_IP=os.getenv('SOURCE_REMOTE_BIND_IP')
SOURCE_REMOTE_BIND_PORT=int(os.getenv('SOURCE_REMOTE_BIND_PORT'))

SOURCE_USER=os.getenv('SOURCE_USER')
SOURCE_PASS=os.getenv('SOURCE_PASS')
SOURCE_DATABASE=os.getenv('SOURCE_DATABASE')
SOURCE_ENGINE=os.getenv('SOURCE_ENGINE')

TARGET_USER=os.getenv('TARGET_USER')
TARGET_PASS=os.getenv('TARGET_PASS')
TARGET_HOST=os.getenv('TARGET_HOST')
TARGET_PORT=os.getenv('TARGET_PORT')
TARGET_DATABASE=os.getenv('TARGET_DATABASE')
TARGET_ENGINE=os.getenv('TARGET_ENGINE')

N_DAYS=9


def main():
    from tqdm import tqdm
    from sqlalchemy import or_,and_,func,cast,Date
    import models
    from sshtunnel import SSHTunnelForwarder
    import utils
    from datetime import datetime
    import pytz
    
    started_at = datetime.now(tz=pytz.timezone('Asia/Jakarta'))
    total_inserted_row = 0
    total_updated_row = 0
    errors = []
    
    
    mysql_engine = utils.engine_func( TARGET_USER,
                                     TARGET_PASS,
                                     TARGET_HOST,
                                     TARGET_PORT,
                                     TARGET_DATABASE,
                                     'mysql' 
                                     )
    
    
    # models.metadata_obj.create_all(bind=mysql_engine)
    models_obj = models.metadata_obj.tables.values() 
    # models_obj = [models.reports]

    
    pbar = tqdm(models_obj)
    
    for i in pbar:
        if i.__str__() == 'MigrationLog':
            continue
        else:
            pbar.set_description(f'Processing {i}')
            
            created_n_days = utils.createdAt_n_days_func(N_DAYS)
            try:
                with SSHTunnelForwarder(
                        (SOURCE_SSH_HOST,SOURCE_SSH_PORT),
                        ssh_username=SOURCE_SSH_USER,
                        ssh_password=SOURCE_SSH_PASS,
                        remote_bind_address=(SOURCE_REMOTE_BIND_IP,SOURCE_REMOTE_BIND_PORT)) as server:
                    server.start()
                    ps_engine = utils.engine_func( SOURCE_USER,
                                        SOURCE_PASS,
                                        server.local_bind_host,
                                        server.local_bind_port,
                                        SOURCE_DATABASE,
                                        'postgresql' 
                                        )
                
                    fetch_source = utils.fetch_filter(i,ps_engine,i.c.updated_at > created_n_days  )
            except Exception as e:
                logging.error(str(e))
                utils.log_func(i, mysql_engine, 'FAIL', 'ERROR', str(e))
                errors.append(i.__str__())
                continue
            
            try:
                inserted_rows,updated_rows = utils.migrate_data(i, mysql_engine, fetch_source)  
            except Exception as e:
                logging.error(str(e))
                utils.log_func(i, mysql_engine, 'FAIL', 'ERROR', str(e))
                errors.append(i.__str__())
                continue
            
            total_inserted_row += inserted_rows
            total_updated_row += updated_rows

            utils.log_func(i, mysql_engine, 'POST', 'SUCCESS', f'{len(fetch_source)} rows retrieved. Migration Done')
    
    if len(errors) < 1:
        utils.monitoring_etl('Lost and Found',mysql_engine,started_at,total_inserted_row,total_updated_row,'Success')
    else:
        e = ', '.join(errors)
        utils.monitoring_etl('Lost and Found',mysql_engine,started_at,total_inserted_row,total_updated_row,f'Fail : {e}')
    
    utils.del_log(mysql_engine,30)
    print("Migration Done")
                
                

if __name__ == '__main__':
    main()