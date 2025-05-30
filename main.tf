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
  depends_on = [
    docker_network.solution_network
  ]
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
  depends_on = [
    docker_network.solution_network
  ]
}

resource "docker_image" "consumer_app" {
  name = "consumer-app:latest"
  build {
    context   = "./consumer-app"
  }
}

resource "docker_image" "producer_flask_app" {
  name = "producer-app:latest"
  build {
    context   = "./producer-app"
  }
}


resource "docker_container" "consumer_app" {
  name  = "consumer-app-container"
  image = docker_image.consumer_app.name

  networks_advanced {
    name = docker_network.solution_network.name
  }

  env = [
    "MYSQL_USER=${var.maria_db_user}",
    "MYSQL_PASSWORD=${var.maria_db_password}",
    "MYSQL_DATABASE=${var.maria_db_db}",
  ]

  ports {
    internal = 8080
    external = 8080
  }
  depends_on = [
    docker_network.solution_network, docker_container.consumer_app
  ]
}

resource "docker_container" "producer_flask_app" {
  name  = "producer-flask-app-container"
  image = docker_image.producer_flask_app.name

  networks_advanced {
    name = docker_network.solution_network.name
  }

  ports {
    internal = 5000
    external = 5000
  }

  depends_on = [
    docker_network.solution_network
  ]
}

output "flask_app_url" {
  description = "URL of the Flask application"
  value       = "http://${docker_container.producer_flask_app.name}:5000"
}