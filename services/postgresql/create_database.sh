#!/env/bash

/etc/init.d/postgresql start

CREATE_COMMAND="CREATE USER $USERNAME WITH SUPERUSER PASSWORD '$PASSWORD';"
psql --echo-all --echo-queries --command "$CREATE_COMMAND"

createdb --echo -O $USERNAME $DATABASE
