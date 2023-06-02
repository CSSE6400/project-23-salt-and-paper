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
    name = "${aws_ecr_repository.saltandpaper_worker.repository_url}:latest" 
    build {
        dockerfile = "./Dockerfile.worker"
        context = "."
        build_arg = {
            SQLALCHEMY_DATABASE_URI = "postgresql://${aws_db_instance.database.username}:${aws_db_instance.database.password}@${aws_db_instance.database.address}:${aws_db_instance.database.port}/${aws_db_instance.database.db_name}",
            CELERY_BROKER_URL = "sqs://", 
            CELERY_RESULT_BACKEND = "db+postgresql://${aws_db_instance.database.username}:${aws_db_instance.database.password}@${aws_db_instance.database.address}:${aws_db_instance.database.port}/${aws_db_instance.database.db_name}"
        }
    }
} 
 
resource "docker_registry_image" "saltandpaper_worker" { 
    name = docker_image.saltandpaper_worker.name 
}