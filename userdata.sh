#!/bin/bash
# Run as root on Amazon Linux 2 or Ubuntu (adjust package manager accordingly)
set -x

# Install essentials
if [ -f /etc/os-release ]; then
  . /etc/os-release
  if [ "$ID" = "amzn" ] || [ "$ID" = "amazon" ]; then
    yum update -y
    yum install -y git python3 python3-devel python3-pip nginx
  else
    apt-get update -y
    apt-get install -y git python3 python3-venv python3-pip nginx
  fi
fi

# Install and configure CloudWatch agent (optional)
# awslogs or unified CloudWatch agent can be installed; skipping for brevity

# Clone repo
cd /home/ec2-user
git clone https://github.com/vaibhqvv/Docscribe.git
chown -R ec2-user:ec2-user Docscribe

# Setup python venv and install requirements (backend)
cd /home/ec2-user/Docscribe/server
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Setup python venv and install requirements (client)
cd /home/ec2-user/Docscribe/client
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Create systemd service for FastAPI (uvicorn)
cat <<'EOF' > /etc/systemd/system/docscribe-backend.service
[Unit]
Description=Docscribe FastAPI
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/Docscribe/server
Environment="PATH=/home/ec2-user/Docscribe/server/venv/bin"
ExecStart=/home/ec2-user/Docscribe/server/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Streamlit
cat <<'EOF' > /etc/systemd/system/docscribe-client.service
[Unit]
Description=Docscribe Streamlit
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/Docscribe/client
Environment="PATH=/home/ec2-user/Docscribe/client/venv/bin"
ExecStart=/home/ec2-user/Docscribe/client/venv/bin/streamlit run app.py --server.address 127.0.0.1 --server.port 8501
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start services
systemctl daemon-reload
systemctl enable docscribe-backend
systemctl start docscribe-backend
systemctl enable docscribe-client
systemctl start docscribe-client

# Configure Nginx reverse proxy (map /api to backend, root to streamlit)
cat <<'EOF' > /etc/nginx/conf.d/docscribe.conf
server {
    listen 80;
    server_name _;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://127.0.0.1:8501/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

systemctl restart nginx
