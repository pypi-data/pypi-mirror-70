TODO
----


* Verificar se é um IP LOCAL e não consultar reverso/dns/ipinfo.


/var/log/dovecot/debbuger.log

May 26 02:06:54 imap-login: Info: Login: user=<francisco@andrefigueiredoimoveis.com.br>, method=PLAIN, rip=52.125.128.18, lip=177.66.160.217, mpid=21031, secured, session=<wfgiJYamoMs0fYAS>
May 26 02:06:55 pop3-login: Info: Login: user=<anderson@naclub.com.br>, method=PLAIN, rip=177.135.75.210, lip=172.16.1.246, mpid=22511, secured, session=<cqQrJYamnfaxh0vS>
May 26 02:06:55 pop3-login: Info: Login: user=<contato@classeempreendimentos.com.br>, method=PLAIN, rip=179.83.21.130, lip=172.16.1.246, mpid=24108, secured, session=<0a8uJYam1s2zUxWC>
May 26 02:06:55 pop3-login: Info: Login: user=<ricardo@biobless.com.br>, method=PLAIN, rip=52.96.56.197, lip=172.16.1.246, mpid=24893, secured, session=<MScwJYamqBg0YDjF>
May 26 02:06:55 pop3(anderson@naclub.com.br)<22511><cqQrJYamnfaxh0vS>: Info: Disconnected: Logged out top=0/0, retr=0/0, del=0/0, size=0
May 26 02:06:55 pop3(contato@classeempreendimentos.com.br)<24108><0a8uJYam1s2zUxWC>: Info: Disconnected: Logged out top=0/0, retr=0/0, del=0/5, size=88707
May 26 02:06:55 pop3-login: Info: Login: user=<financeiro@classeempreendimentos.com.br>, method=PLAIN, rip=179.83.21.130, lip=172.16.1.246, mpid=26675, secured, session=<X4A1JYam2M2zUxWC>
May 26 02:06:56 pop3(financeiro@classeempreendimentos.com.br)<26675><X4A1JYam2M2zUxWC>: Info: Disconnected: Logged out top=0/0, retr=0/0, del=0/14, size=440133



root@crow:/var/log/dovecot # grep method debbuger.log | awk '{ print $8 }' | sort -n | uniq -c
5643 failed,
148960 method=PLAIN,






