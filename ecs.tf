# Code mostly taken from [3]
resource "aws_ecs_cluster" "saltandpaper" {
    name = "saltandpaper"
}

resource "aws_ecs_task_definition" "saltandpaper_task" {
    family                   = "saltandpaper_task"
    network_mode             = "awsvpc"
    requires_compatibilities = ["FARGATE"]
    cpu                      = 1024
    memory                   = 2048
    execution_role_arn       = data.aws_iam_role.lab.arn
    task_role_arn            = data.aws_iam_role.lab.arn

    container_definitions = <<DEFINITION
[
    {
        "image": "${docker_image.saltandpaper.name}",
        "cpu": 512,
        "memory": 1024,
        "name": "backend",
        "networkMode": "awsvpc",
        "portMappings": [
        {
            "containerPort": 6400,
            "hostPort": 6400
        }
        ],
         "environment": [
            {
                "name": "SQLALCHEMY_DATABASE_URI",
                "value": "postgresql://${local.database_username}:${local.database_password}@${aws_db_instance.database.address}:${aws_db_instance.database.port}/${aws_db_instance.database.db_name}"
            },
            {
                "name": "JSON_SORT_KEYS",
                "value": "false"
            },
            {
                "name": "CELERY_BROKER_URL",
                "value": "sqs://"
            },
            {
                "name": "CELERY_RESULT_BACKEND",
                "value": "db+postgresql://${local.database_username}:${local.database_password}@${aws_db_instance.database.address}:${aws_db_instance.database.port}/${aws_db_instance.database.db_name}"
            }
        ],
        "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "/saltandpaper/backend",
            "awslogs-region": "us-east-1",
            "awslogs-stream-prefix": "ecs",
            "awslogs-create-group": "true"
        }
        }
    },
    {
        "image": "${docker_image.saltandpaper_worker.name}",  
        "cpu": 512,
        "memory": 1024,
        "name": "celery-worker",
        "networkMode": "awsvpc",
         "environment": [
            {
                "name": "SQLALCHEMY_DATABASE_URI",
                "value": "postgresql://${local.database_username}:${local.database_password}@${aws_db_instance.database.address}:${aws_db_instance.database.port}/${aws_db_instance.database.db_name}"
            },
            {
                "name": "CELERY_BROKER_URL",
                "value": "sqs://"
            },
            {
                "name": "CELERY_RESULT_BACKEND",
                "value": "db+postgresql://${local.database_username}:${local.database_password}@${aws_db_instance.database.address}:${aws_db_instance.database.port}/${aws_db_instance.database.db_name}"
            }
        ],
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "/saltandpaper/celery-worker",
                "awslogs-region": "us-east-1",
                "awslogs-stream-prefix": "ecs",
                "awslogs-create-group": "true"
            }
        }
    }

]
DEFINITION
}

resource "aws_ecs_service" "saltandpaper_ecs" {
    name            = "saltandpaper"
    cluster         = aws_ecs_cluster.saltandpaper.id
    task_definition = aws_ecs_task_definition.saltandpaper_task.arn
    desired_count   = 2
    launch_type     = "FARGATE"

    network_configuration {
        subnets             = data.aws_subnets.private.ids
        security_groups     = [aws_security_group.saltandpaper_ecs.id]
        assign_public_ip    = true
    }
    load_balancer { 
        target_group_arn = aws_lb_target_group.saltandpaper_lb.arn 
        container_name   = "backend" 
        container_port   = 6400 
    }

}

resource "aws_security_group" "saltandpaper_ecs" {
    name = "saltandpaper_ecs"
    description = "Salt and Paper Security Group"

    ingress {
        from_port = 6400
        to_port = 6400
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

