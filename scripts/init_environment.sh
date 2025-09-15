#!/usr/bin/env sh

# Exit on error
set -e

. "$(dirname "$0")/load_dotenv.sh"

SCRIPT_PATH="$0"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
STACK_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TRAEFIK_DIR="$(cd "$STACK_DIR/.." && pwd)/traefik"
log() {
    level="$1"
    shift
    echo "[$level] $*" >&2
}

generate_password() {
    length=$1
    char_set="A-Za-z0-9!@#$%^&*()-_=+[]{}|;:,.<>?"
    tr -dc "$char_set" </dev/urandom | head -c "$length"
    echo
}

setup_traefik() {
    create_traefik_network_if_needed
    
    log INFO "Setting up Traefik reverse proxy in $TRAEFIK_DIR"
    mkdir -p "$TRAEFIK_DIR"
    ln -sf "$STACK_DIR/docker-compose.traefik.yml" "$TRAEFIK_DIR/docker-compose.yml"
    touch "$TRAEFIK_DIR/.env"

    PASSWORD=$(generate_password 15)
    log INFO "Generated Traefik dashboard password: $PASSWORD"

    HASHED_PASSWORD=$(openssl passwd -apr1 "$PASSWORD")

    cat > "$TRAEFIK_DIR/.env" <<EOF
USERNAME=admin
HASHED_PASSWORD='$HASHED_PASSWORD'
DOMAIN=$DOMAIN
EMAIL=admin@$DOMAIN
ALLOWED_IPS=
EOF

    log INFO "Traefik .env file created at $TRAEFIK_DIR/.env"
}


wait_for_traefik_dashboard() {
    dashboard_url="https://traefik.${DOMAIN}"

    log INFO "Waiting for Traefik dashboard at $dashboard_url..."

    i=0
    while [ "$i" -lt 60 ]; do
        status_code=$(curl -sk -o /dev/null -w "%{http_code}" "$dashboard_url" || echo "000")
        if [ "$status_code" = "200" ] || [ "$status_code" = "401" ] || [ "$status_code" = "403" ]; then
            log INFO "Traefik dashboard is up (HTTP $status_code)."
            return
        fi
        sleep 2
        i=$((i + 1))
    done

    log ERROR "Traefik dashboard did not become ready in time."
    exit 1
}
create_traefik_network_if_needed() {
    log INFO "Checking if the Traefik network exists..."
    
    if ! sudo docker network ls | grep -q "traefik-public"; then
        log INFO "Creating Traefik network..."
        sudo docker network create traefik-public
    else
        log INFO "Traefik network already exists."
    fi
}


main() {
    load_dotenv

    log INFO "Initializing environment..."

    setup_traefik

    log INFO "Starting Traefik..."
    (cd "$TRAEFIK_DIR" && sudo docker compose up -d)
    wait_for_traefik_dashboard


    log INFO "Initialization complete."
}

main
