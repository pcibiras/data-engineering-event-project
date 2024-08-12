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

resource "docker_network" "solution-network" {
  name = "solution-network"
}

resource "docker_image" "nats" {
  name = "nats:latest"
}

resource "docker_container" "nats" {
  image = docker_image.nats.name
  name  = "nats"
  networks_advanced {
  name = docker_network.solution-network.name
  }

  ports {
    internal = 4222
    external = 4222
  }
}
