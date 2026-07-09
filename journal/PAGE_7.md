# PAGE 7

## time: 09.07.2026, 21:28 EET 

After the `bootstrap.sh` script finishes its execution, you need to perform the following actions:
- copy the public key from the `shared_folder` inside the `C:\ProgramData\ssh\administrators_authorized_keys`
- create `.vault_pass` file inside '/home/student'
- create `group_vars/vault.yml` and paste the required secrets
- make sure that you have the `inventory` file inside `inventories` folder and inside use the hypervisor host correct 
IPv4 address


I managed to create a procedure for the creation of a master node. This is the `bootstrap.sh` script:

```commandline
#!/bin/bash
set -e 

dnf update -y

# CREATE THE 'student' USER

useradd -m -s /bin/bash student || true
echo 'student:Bursuc123' | chpasswd
usermod -aG wheel student

echo 'student ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/90-vagrant-users
chmod 440 /etc/sudoers.d/90-vagrant-users

echo 'PasswordAuthentication yes' > /etc/ssh/sshd_config.d/50-password-auth.conf
chmod 600 /etc/ssh/sshd_config.d/50-password-auth.conf

systemctl restart sshd

# GENERATE THE SSH KEY

sudo -u student bash -c '
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
'

cp /home/student/.ssh/id_ed25519.pub /home/vagrant/shared/

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

sudo -u student bash -c 'echo "export VAULT_PASSWORD=Bursuc123" >> /home/student/venvs/venv/bin/activate'
sudo -u student bash -c 'echo "export DJANGO_SETTINGS_MODULE=api_config.settings" >> /home/student/venvs/venv/bin/activate'

sudo -u student bash -c 'echo "source ~/venvs/venv/bin/activate" >> /home/student/.bash_profile'

sudo -u student bash -c '
cd /home/student
git clone https://github.com/DraghiciAndrei1307/PostgreSQL-Ansible-Automation.git
cd PostgreSQL-Ansible-Automation
cd ansible

mkdir inventories
chmod 755 inventories

mkdir provisioning_logs
chmod 755 provisioning_logs

mkdir group_vars
chmod 755 group_vars
'

# INSTALL THE PYTHON PACKAGES

/home/student/venvs/venv/bin/pip install --upgrade pip

/home/student/venvs/venv/bin/pip install ansible

/home/student/venvs/venv/bin/pip install https://github.com/DraghiciAndrei1307/PostgreSQL-Python-Automation/releases/download/os_runner-v0.0.1/os_runner_draghici_andrei-0.0.1-py3-none-any.whl

/home/student/venvs/venv/bin/pip install https://github.com/DraghiciAndrei1307/PostgreSQL-Python-Automation/releases/download/pg_provisioner-v0.0.4/pg_provisioner_draghici_andrei-0.0.4-py3-none-any.whl

/home/student/venvs/venv/bin/pip install https://github.com/DraghiciAndrei1307/PostgreSQL-Python-Automation/releases/download/django_rest_api-v0.0.6/django_rest_api_draghici_andrei-0.0.6-py3-none-any.whl

# CONFIGURE DJANGO PREREQUISITES

sudo -u student bash -c '
export DJANGO_SETTINGS_MODULE=api_config.settings
export VAULT_PASSWORD=Bursuc123
/home/student/venvs/venv/bin/migrate-pg-api migrate
/home/student/venvs/venv/bin/pg-api-create-superuser -u admin -e admin@example.com -p 1234
'

# OPEN DJANGO(9001) and FLOWER(5555) PORTS

systemctl enable --now firewalld
sudo firewall-cmd --permanent --add-port=9001/tcp
sudo firewall-cmd --permanent --add-port=5555/tcp
sudo firewall-cmd --reload

# CONFIGURE REDIS, CELERY AND FLOWER

dnf install -y redis
systemctl enable --now redis

/home/student/venvs/venv/bin/pip install "celery[redis]" flower

sudo -u student bash -c '
export DJANGO_SETTINGS_MODULE=api_config.settings
export VAULT_PASSWORD=Bursuc123
nohup /home/student/venvs/venv/bin/celery -A provisioner_api.tasks worker --loglevel=info >/home/student/celery.log 2>&1 &
nohup /home/student/venvs/venv/bin/run-pg-api >/home/student/django.log 2>&1 &
'

```

What I am going to do tomorrow is to integrate the backup logic with the Django API and then use Celery + Celery Beat 
to create a "reconcile" loop and perform some tests. 

Also, after I finish with this Celery setup, I will also try to create some additional master nodes that are provisioned
with different schedulers like Chroniker, APScheduler, Django-Q(Django-Q2) or other similar things. 
