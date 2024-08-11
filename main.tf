terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "kafka_network" {
  name = "kafka-network"
}

# resource "docker_container" "zookeeper" {
#   image = "confluentinc/cp-zookeeper:latest"
#   name  = "zookeeper"

#   networks_advanced {
#     name = docker_network.kafka_network.name
#   }

#   env = [
#     "ZOOKEEPER_CLIENT_PORT = 2181"
#   ]
# }

# resource "docker_image" "zookeeper" {
#   name = "confluentinc/cp-zookeeper:latest"
# }

# resource "docker_image" "zookeeper" {
#   name = "bitnami/zookeeper:latest"
# }   

resource "docker_image" "nats" {
  name = "nats:latest"
}

resource "docker_container" "nats" {
  image = docker_image.nats.name
  name  = "nats"

  ports {
    internal = 4222
    external = 4222
  }
}

resource "docker_image" "postgres-14-image" {
  name = "postgres:14.0"
}

resource "docker_container" "postgres-container" {
  image = docker_image.postgres-14-image.name  # Use the PostgreSQL image version you prefer
  name  = "postgres_db"
  networks_advanced {
    name = docker_network.kafka_network.name
  }
    ports {
    internal = 5432
    external = 5432
  }
    volumes {
    host_path = "/data"
    container_path = "/var/lib/postgresql/data"
  }
  env [
    "POSTGRES_USER = {var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}" 
  ]
}
