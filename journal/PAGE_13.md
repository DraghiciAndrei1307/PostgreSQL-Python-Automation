# PAGE 13

## time: 30.08.2026, 18:00 EET 

LOG:

1) Decided to start with the `step 1` and update the `provisioning + backup` (after the provisioning) workflow logic. 
2) The first step will be to update the `Vagrantfile` to create an "infrastructure-base" VM which I will use to create 
2 clones (the INF VMs) for the SLAVE VM during the provisioning process.  

I updated the Vagrantfile like this: 

```bash

# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "generic/rocky9"

  config.vm.synced_folder "./shared_folder", "/home/vagrant/shared"  

  config.vm.define "master-celery-redis" do |celery_redis|

    celery_redis.vm.provision "shell", path: "./scripts/bootstrap_celery_celery_beat_redis.sh"

    celery_redis.vm.provider "virtualbox" do |v|

      v.name = "master-celery-redis"
      v.linked_clone = true

    end

    celery_redis.vm.hostname = "master-celery-redis"
    celery_redis.vm.network "public_network", bridge: "Intel(R) Wi-Fi 6 AX200 160MHz"

  end

  config.vm.define "infrastructure-base" do |infrastructure_base|
    
    infrastructure_base.vm.provider "virtualbox" do |v|
    
      v.name = "infrastructure-base"
      v.linked_clone = true 
 
    end
    
    infrastructure_base.vm.hostname = "infrastructure-base"
    infrastructure_base.vm.network "public_network", bridge: "Intel(R) Wi-Fi 6 AX200 160MHz"

  end	

end

```

And the `boostrap` script like this: 

```bash

#!/bin/bash
set -e 

dnf update -y

# CREATE THE 'student' USER

useradd -m -s /bin/bash student || true
echo 'student:<some_password>' | chpasswd
usermod -aG wheel student

echo 'student ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/90-vagrant-users
chmod 440 /etc/sudoers.d/90-vagrant-users

echo 'PasswordAuthentication yes' > /etc/ssh/sshd_config.d/50-password-auth.conf
chmod 600 /etc/ssh/sshd_config.d/50-password-auth.conf

systemctl restart sshd

# GENERATE THE SSH KEY

sudo -u student bash -c '
ssh-keygen -t ed25519 -f ~/.ssh/master_celery_redis_ssh_key -N ""

cat > ~/.ssh/config <<EOF
Host 192.168.1.181
    User andrei
    IdentityFile ~/.ssh/master_celery_redis_ssh_key
EOF
chmod 600 ~/.ssh/config
'

cp /home/student/.ssh/master_celery_redis_ssh_key.pub /home/vagrant/shared/

# INSTALL GIT

dnf install -y git-all

# INSTALL python3.12

dnf install -y python3.12

# INSTALL arp-scan

dnf install epel-release -y
dnf install -y arp-scan

# CONFIGURE THE venv

sudo -u student mkdir -p /home/student/venvs

sudo -u student python3.12 -m venv /home/student/venvs/venv

sudo -u student bash -c 'echo "export VAULT_PASSWORD=<some_password>" >> /home/student/venvs/venv/bin/activate'
sudo -u student bash -c 'echo "export DJANGO_SETTINGS_MODULE=django_api.settings" >> /home/student/venvs/venv/bin/activate'

sudo -u student bash -c 'echo "source ~/venvs/venv/bin/activate" >> /home/student/.bash_profile'

# INSTALL THE PYTHON PACKAGES

/home/student/venvs/venv/bin/pip install --upgrade pip

/home/student/venvs/venv/bin/pip install ansible

/home/student/venvs/venv/bin/pip install https://github.com/DraghiciAndrei1307/PostgreSQL-Python-Automation/releases/download/os_runner-v0.0.1/os_runner_draghici_andrei-0.0.1-py3-none-any.whl

/home/student/venvs/venv/bin/pip install https://github.com/DraghiciAndrei1307/PostgreSQL-Python-Automation/releases/download/pg_provisioner-v0.0.4/pg_provisioner_draghici_andrei-0.0.4-py3-none-any.whl

/home/student/venvs/venv/bin/pip install https://github.com/DraghiciAndrei1307/PostgreSQL-Python-Automation/releases/download/django_rest_api-v0.0.1/django_rest_api_draghici_andrei-0.0.1-py3-none-any.whl

# Install Celery and Flower

/home/student/venvs/venv/bin/pip install "celery[redis]" flower

# CONFIGURE THE INVENTORY

sudo -u student bash -c '
cd /home/student

touch .vault_pass
echo "<some_password>" >> .vault_pass

git clone https://github.com/DraghiciAndrei1307/PostgreSQL-Ansible-Automation.git
cd PostgreSQL-Ansible-Automation
cd ansible

mkdir inventories
chmod 755 inventories

cd inventories

touch inventory
chmod 644 inventory

echo "hypervisor ansible_connection=ssh ansible_host=192.168.1.xxx ansible_user=Andrei ansible_remote_tmp=C:/Users/Andrei/AppData/Local/Temp/.ansible ansible_shell_type=powershell" >> inventory

cd .. 

mkdir provisioning_logs
chmod 755 provisioning_logs

mkdir group_vars
chmod 755 group_vars

cd group_vars

touch vault.yml

tee vault.yml > /dev/null <<EOF
ansible_user: student
ansible_password: <some_password>
ansible_become_password: <some_password>

redhat_username: "email"
redhat_password: "password"

django_admin: admin
django_password: 1234
EOF

/home/student/venvs/venv/bin/ansible-vault encrypt vault.yml \
    --vault-password-file /home/student/.vault_pass \
    --encrypt-vault-id default
'

# --encrypt-vault-id default makes this (the file) 
# VAULT password the default source from which the password 
# is used 

# CONFIGURE DJANGO PREREQUISITES

sudo -u student bash -c '
export DJANGO_SETTINGS_MODULE=django_api.settings
export VAULT_PASSWORD=<some_password>
/home/student/venvs/venv/bin/migrate-pg-api migrate
/home/student/venvs/venv/bin/pg-api-create-superuser -u admin -e admin@example.com -p 1234
'

# OPEN DJANGO(9001) and FLOWER(5555) PORTS

systemctl enable --now firewalld
sudo firewall-cmd --permanent --add-port=9001/tcp
sudo firewall-cmd --permanent --add-port=5555/tcp
sudo firewall-cmd --reload

# ---- CONFIGURE REDIS, CELERY AND FLOWER ---- #

# Install and Enable Redis

dnf install -y redis
systemctl enable --now redis

touch /etc/default/celery

# Configure the enviromet variables for Celery(to keep the systemd files clean) 

echo "CELERY_APP=django_api" >> /etc/default/celery
echo "CELERY_BIN=/home/student/venvs/venv/bin/celery" >> /etc/default/celery
echo "CELERY_POOL=threads" >> /etc/default/celery
echo "CELERY_CONCURRENCY=16" >> /etc/default/celery
echo "CELERY_LOG_LEVEL=INFO" >> /etc/default/celery

# Create and configure startup scripts

touch /usr/local/bin/run_celery.sh
touch /usr/local/bin/run_celerybeat.sh

echo '#!/bin/bash' >> /usr/local/bin/run_celery.sh
echo 'source /etc/default/celery' >> /usr/local/bin/run_celery.sh
echo 'source /home/student/venvs/venv/bin/activate' >> /usr/local/bin/run_celery.sh
echo 'exec $CELERY_BIN -A $CELERY_APP worker --pool=$CELERY_POOL --concurrency=$CELERY_CONCURRENCY -l $CELERY_LOG_LEVEL' >> /usr/local/bin/run_celery.sh

echo '#!/bin/bash' >> /usr/local/bin/run_celerybeat.sh
echo 'source /etc/default/celery' >> /usr/local/bin/run_celerybeat.sh
echo 'source /home/student/venvs/venv/bin/activate' >> /usr/local/bin/run_celerybeat.sh
echo 'exec $CELERY_BIN -A $CELERY_APP beat -l $CELERY_LOG_LEVEL' >> /usr/local/bin/run_celerybeat.sh

chmod +x /usr/local/bin/run_celery.sh
chmod +x /usr/local/bin/run_celerybeat.sh

# Create Systemd Service for Celery Worker

touch /etc/systemd/system/celery.service

tee /etc/systemd/system/celery.service > /dev/null <<EOF
[Unit]
Description=Celery Worker Service
After=network.target redis.service

[Service]
User=student
Group=student
WorkingDirectory=/home/student
EnvironmentFile=/etc/default/celery
Environment="DJANGO_SETTINGS_MODULE=django_api.settings"
ExecStart=/usr/local/bin/run_celery.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Create Systemd Service for Celery Beat

touch /etc/systemd/system/celerybeat.service 

tee /etc/systemd/system/celerybeat.service > /dev/null <<EOF
[Unit]
Description=Celery Beat Scheduler
After=network.target

[Service]
User=student
Group=student
WorkingDirectory=/home/student
EnvironmentFile=/etc/default/celery
Environment="DJANGO_SETTINGS_MODULE=django_api.settings"
ExecStart=/usr/local/bin/run_celerybeat.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services

systemctl daemon-reload
systemctl enable celery
systemctl enable celerybeat
systemctl start celery
systemctl start celerybeat

sudo -u student bash -c '
export DJANGO_SETTINGS_MODULE=django_api.settings
export VAULT_PASSWORD=<some_password>
nohup /home/student/venvs/venv/bin/run-pg-api >/home/student/django.log 2>&1 &
'

# The followig line was in the last group of commands

# nohup /home/student/venvs/venv/bin/celery -A django_api worker --loglevel=info >/home/student/celery.log 2>&1 &

```

3) The things that the client needs to do after the Master node was created are: 
- update the bootstrap script with the actual IP Address of the hypervisor host
- copy the public key of the master VM into the C:\ProgramData\ssh\administrators_authorized_keys file from the hypervisor host 
- update the ansible/inventories/inventory with the actual IP Address of the hypervisor host 
- update the group_vars/vault.yml with the actual values of the secrets

4) I am thinking that I should create another branch with all the files that I have on my host hypervisor host. I think 
that this approach will make the system more robust. 

Another approach would be to move to VMs that I create inside Proxmox and use the KVM approach or simply use containers 
k8s. This implies significant changes to my project though. I need to consider this in the future. 

For the moment, what I have will do just fine. 

