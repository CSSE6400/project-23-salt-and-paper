# Code mostly taken from [3]
resource "docker_image" "saltandpaper" { 
    name = "${aws_ecr_repository.saltandpaper.repository_url}:latest" 
    build {
        dockerfile = "./Dockerfile"
        context = "."
    }
} 
 
resource "docker_registry_image" "saltandpaper" { 
    name = docker_image.saltandpaper.name 
}

resource "docker_image" "saltandpaper_worker" { 
    name = "${aws_ecr_repository.saltandpaper_worker.repository_url}:14" 
    build {
        dockerfile = "./Dockerfile.worker"
        context = "."
    }
} 
 
resource "docker_registry_image" "saltandpaper_worker" { 
    name = docker_image.saltandpaper_worker.name 
}