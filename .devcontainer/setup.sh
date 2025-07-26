apt-get update
apt-get install -y python3 python3-pip curl

# Install Go
curl -sSL https://go.dev/dl/go1.22.0.linux-amd64.tar.gz -o go.tar.gz
rm -rf /usr/local/go
tar -C /usr/local -xzf go.tar.gz
ln -s /usr/local/go/bin/go /usr/local/bin/go

# Optionally install docker-compose inside container if needed
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

go version
docker --version
docker-compose version || echo "docker-compose not installed"
