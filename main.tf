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

resource "docker_network" "solution_network" {
  name = "solution-network"
}

resource "docker_image" "nats" {
  name = "nats:latest"
}

resource "docker_container" "nats" {
  image = docker_image.nats.name
  name  = "nats"
  networks_advanced {
  name = docker_network.solution_network.name
  }

  ports {
    internal = 4222
    external = 4222
  }
}

resource "docker_image" "mariadb" {
  name = "mariadb:latest"
}

resource "docker_container" "mariadb_db" {
  image = docker_image.mariadb.name
  name  = "mariadb_db"

  networks_advanced {
    name = docker_network.solution_network.name
  }
   volumes {
    host_path      = "/home/povilas/mariadb_data"
    container_path = "/var/lib/mysql"
  }
  ports {
    internal = 3306
    external = 3306
  }
   env = [
    "MYSQL_ROOT_PASSWORD=${var.maria_db_root_password}",
    "MYSQL_DATABASE=${var.maria_db_db}",
    "MYSQL_USER=${var.maria_db_user}",
    "MYSQL_PASSWORD=${var.maria_db_password}"
  ]
}

resource "docker_image" "consumer_app" {
  name = "consumer-app:latest"
  build {
    context    = "./consumer-app"
  }
}

