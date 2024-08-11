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
