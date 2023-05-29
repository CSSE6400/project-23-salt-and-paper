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
